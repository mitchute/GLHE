from math import log, pi

from numpy import genfromtxt
from scipy.interpolate import interp1d

from glhe.aggregation.aggregation_factory import make_aggregation
from glhe.aggregation.dynamic_bin import DynamicBin
from glhe.g_function.flow_fraction import FlowFraction
from glhe.globals.functions import merge_dicts
from glhe.ground_temps.ground_temp_factory import make_ground_temp_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.properties.base_properties import PropertiesBase
from glhe.properties.fluid_properties import Fluid
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class GFunction(SimulationEntryPoint):
    def __init__(self, inputs):
        self.inputs = inputs

        # g-function properties
        g_functions = genfromtxt(inputs['g-functions']['file'], delimiter=',')

        self.g_function_interp = interp1d(g_functions[:, 0],
                                          g_functions[:, 1],
                                          fill_value='extrapolate')

        self.fluid = Fluid(inputs['fluid'])
        self.soil = PropertiesBase(inputs=inputs['soil'])

        # initialize time here
        self.sim_time = 0

        # init load aggregation method
        self.load_aggregation = make_aggregation(inputs['load-aggregation'])

        # ground temperature model
        self.get_ground_temp = make_ground_temp_model(merge_dicts(inputs['ground-temperature'],
                                                                  {'soil-diffusivity': self.soil.diffusivity}
                                                                  )).get_temp

        self.my_bh = SingleUTubeGroutedBorehole(merge_dicts(inputs['g-functions']['borehole-data'],
                                                            {'initial temp': self.get_ground_temp(0, 100)}), self.fluid,
                                                self.soil)

        self.flow_frac = FlowFraction()

        self.NUM_BH = inputs['g-functions']['number of boreholes']
        self.TOT_LENGTH = self.my_bh.length * self.NUM_BH

        # time constant
        self.t_s = self.my_bh.length ** 2 / (9 * self.soil.diffusivity)

        self.c_0 = 2 * pi * self.soil.conductivity

        # initial temperature
        init_temp = self.get_ground_temp(time=self.sim_time, depth=self.my_bh.length)

        # other inits
        self.fluid_cap = 0
        self.bh_resist = 0.15
        self.ground_temp = 0
        self.ave_fluid_temp = init_temp
        self.ave_fluid_temp_change = 0
        self.flow_fraction = 0
        self.load_per_meter = 0
        self.prev_mass_flow_rate = -999
        self.mass_flow_change_fraction_tolerance = 0.05
        self.time_of_curr_flow = 0
        self.time_of_prev_flow = 0
        self.flow_change_fraction_limit = 0.1
        self.prev_sim_time = 0
        self.time_step = 0
        self.curr_total_load = 0
        self.outlet_temp = init_temp
        self.inlet_temp = init_temp

        self.total_pipe_mass = self.my_bh.PIPE_VOL * self.my_bh.pipe.density
        self.total_grout_mass = self.my_bh.GROUT_VOL * self.my_bh.grout.density

        # set initial g-values
        self.load_aggregation.update_time()
        self.update_g_values(False)

    def report_output(self):
        ret_vals = {"Local Borehole Resistance 'Rb' [K/(W/m)]": self.bh_resist,
                    "Total Internal Borehole Resistance 'Ra' [K/(W/m)]": self.my_bh.resist_bh_total_internal,
                    "Flow Fraction [-]": self.flow_fraction,
                    "Load on GHE [W/m]": self.load_per_meter,
                    "Average Fluid Temp [C]": self.ave_fluid_temp,
                    "GHE Outlet Temp [C]": self.outlet_temp,
                    "GHE Inlet Temp [C]": self.inlet_temp}

        return ret_vals

    def update_g_values(self, lock_down_g_value=True):
        for this_bin in self.load_aggregation.loads:
            if this_bin.g_fixed is True:
                break
            else:
                this_bin.g = self.get_g_func(this_bin.time)
                if isinstance(this_bin, DynamicBin) and lock_down_g_value:
                    this_bin.g_fixed = True

    def get_g_func(self, time):
        """
        Retrieves the interpolated g-function value

        :param time: time [s]
        :return: g-function value
        """

        try:
            lntts = log(time / self.t_s)
        except ValueError:  # pragma: no cover
            return 0  # pragma: no cover

        g = float(self.g_function_interp(lntts))

        if (g / (2 * pi * self.soil.conductivity) + self.bh_resist) < 0:
            return -self.bh_resist * 2 * pi * self.soil.conductivity  # pragma: no cover
        else:
            return g

    def simulate_time_step(self, sim_time, time_step, mass_flow_rate, inlet_temp):

        if mass_flow_rate == 0:
            return sim_time, time_step, mass_flow_rate, inlet_temp

        mass_flow_change_fraction = abs(mass_flow_rate - self.prev_mass_flow_rate) / self.prev_mass_flow_rate

        if mass_flow_change_fraction > self.mass_flow_change_fraction_tolerance:
            self.my_bh.set_flow_rate(mass_flow_rate / self.NUM_BH)
            self.bh_resist = self.my_bh.resist_bh_ave

        self.time_step = time_step
        self.inlet_temp = inlet_temp

        if sim_time != self.sim_time:
            self.sim_time = sim_time

            self.load_aggregation.get_new_current_load_bin(width=time_step)
            self.load_aggregation.current_load.g = self.get_g_func(time_step)

            flow_change_frac = abs((mass_flow_rate - self.prev_mass_flow_rate) / mass_flow_rate)

            if flow_change_frac > self.flow_change_fraction_limit:
                self.time_of_prev_flow = self.time_of_curr_flow
                self.time_of_curr_flow = self.sim_time
                self.prev_mass_flow_rate = mass_flow_rate

            self.flow_fraction = self.calc_flow_fraction()
            # self.flow_fraction = 0.5
            self.ground_temp = self.get_ground_temp(time=self.sim_time, depth=self.my_bh.length)
            self.fluid_cap = mass_flow_rate * self.fluid.specific_heat

        temp_rise_prev_bin, q_prev_bin, g_func_prev_bin = self.calc_prev_bin_temp_rise()

        # heat rate (original and Beier)
        load_num_1 = self.inlet_temp - self.ground_temp
        load_num_2 = (q_prev_bin * g_func_prev_bin - self.calc_temp_rise_history()) / self.c_0

        load_den_1 = g_func_prev_bin / self.c_0
        load_den_2 = (1 - self.flow_fraction) * self.TOT_LENGTH / self.fluid_cap + self.bh_resist

        load_num = load_num_1 + load_num_2
        load_den = load_den_1 + load_den_2

        self.load_per_meter = load_num / load_den
        self.curr_total_load = self.load_per_meter * self.TOT_LENGTH
        energy_per_meter = self.load_per_meter * self.time_step
        self.load_aggregation.set_current_load(load=energy_per_meter)

        temp_rise_history = self.calc_temp_rise_history(include_current_timestep=True)
        self.ave_fluid_temp = self.ground_temp + temp_rise_history / self.c_0 + self.load_per_meter * self.bh_resist
        self.outlet_temp = self.ave_fluid_temp - self.flow_fraction * self.curr_total_load / self.fluid_cap

        if converged:
            self.load_aggregation.aggregate()
            self.load_aggregation.update_time()
            self.update_g_values()
            self.prev_sim_time = self.sim_time
            self.fluid.update_properties(self.ave_fluid_temp)

        return self.outlet_temp

    def calc_prev_bin_temp_rise(self):

        try:
            prev_bin = self.load_aggregation.get_most_recent_bin()
            delta_t_prev_bin = prev_bin.time
            q_prev_bin = prev_bin.get_load()
            g_func_prev_bin = self.get_g_func(delta_t_prev_bin)
            temp_rise_prev_bin = q_prev_bin * g_func_prev_bin
        except IndexError:
            temp_rise_prev_bin = 0
            q_prev_bin = 0
            g_func_prev_bin = self.get_g_func(60)

        return temp_rise_prev_bin, q_prev_bin, g_func_prev_bin

    @staticmethod
    def calc_temp_rise(bin_i, bin_i_minus_1):
        load_i = bin_i.get_load()
        load_i_minus_1 = bin_i_minus_1.get_load()
        return (load_i - load_i_minus_1) * bin_i_minus_1.g

    def calc_temp_rise_history(self, include_current_timestep=False):

        temp_rise_sum = 0

        # calculate history
        for i in range(len(self.load_aggregation.loads) - 1):
            bin_i = self.load_aggregation.loads[i]
            bin_i_minus_1 = self.load_aggregation.loads[i + 1]
            temp_rise_sum += self.calc_temp_rise(bin_i, bin_i_minus_1)

        # calculate last bin, if it exists
        try:
            bin_i = self.load_aggregation.loads[-1]
            temp_rise_sum += bin_i.get_load() * bin_i.g
        except IndexError:
            pass

        # include effect of current time-step
        if include_current_timestep:
            bin_i = self.load_aggregation.current_load
            try:
                bin_i_minus_1 = self.load_aggregation.loads[0]
                temp_rise_sum += self.calc_temp_rise(bin_i, bin_i_minus_1)
            except IndexError:
                temp_rise_sum += bin_i.get_load() * bin_i.g

        return temp_rise_sum
