from math import log, exp, sqrt, sin

from numpy import genfromtxt, mean
from scipy.interpolate import interp1d

from glhe.aggregation.dynamic_bin import DynamicBin
from glhe.aggregation.factory import load_agg_factory
from glhe.globals.constants import PI, GAMMA
from glhe.globals.functions import merge_dicts
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.borehole import Borehole


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
        self.load_aggregation = load_agg_factory(inputs['load-aggregation'])

        # response constant
        self.c_0 = 1 / (2 * PI * self.soil.conductivity)

        # ground temperature model
        self.my_ground_temp = make_ground_temperature_model(merge_dicts(inputs['ground-temperature'],
                                                                        {'soil-diffusivity': self.soil.diffusivity}
                                                                        )).get_temp

        self.my_bh = Borehole(inputs['g-functions']['borehole-data'], self.fluid, self.soil)
        self.NUM_BH = inputs['g-functions']['number of boreholes']

        self.TOT_LENGTH = self.my_bh.DEPTH * self.NUM_BH

        # time constant
        self.t_s = self.my_bh.DEPTH ** 2 / (9 * self.soil.diffusivity)

        # initial temperature
        init_temp = self.my_ground_temp(time=self.sim_time, depth=self.my_bh.DEPTH)

        # other inits
        self.fluid_cap = 0
        self.bh_resist = 0.15
        self.soil_resist = 0
        self.ground_temp = 0
        self.ave_fluid_temp = init_temp
        self.prev_ave_fluid_temp = init_temp
        self.flow_fraction = 0
        self.transit_time = 0
        self.load_per_meter = 0
        self.prev_load_normalized = 0
        self.prev_mass_flow_rate = -999
        self.prev_flow_frac = 0
        self.outlet_temp = init_temp
        self.prev_outlet_temp = init_temp
        self.time_of_curr_flow = 0
        self.time_of_prev_flow = 0
        self.flow_change_fraction_limit = 0.1
        self.specific_load_tolerance = 2000
        self.prev_sim_time = 0
        self.time_step = 0
        self.temp_rise_history = 0
        self.curr_total_load = 0

        # set initial g-values
        self.load_aggregation.update_time()
        self.update_g_values(False)

    def report_output(self):
        ret_vals = {"Local Borehole Resistance 'Rb' [K/(W/m)]": self.bh_resist,
                    "Total Internal Borehole Resistance 'Ra' [K/(W/m)]": self.my_bh.resist_bh_total_internal,
                    "Soil Resistance 'Rs' [K/(W/m)]": self.soil_resist,
                    "Flow Fraction [-]": self.flow_fraction,
                    "Load on GHE [W/m]": self.load_per_meter,
                    "Average Fluid Temp [C]": self.ave_fluid_temp}

        return ret_vals

    def update_g_values(self, lock_down_g_value=True):
        for this_bin in self.load_aggregation.loads:
            if this_bin.g_fixed is True:
                pass
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

        if (g / (2 * PI * self.soil.conductivity) + self.bh_resist) < 0:
            return -self.bh_resist * 2 * PI * self.soil.conductivity  # pragma: no cover
        else:
            return g

    def simulate_time_step(self, inlet_temp, mass_flow, time_step, first_pass, converged):
        if first_pass:
            self.time_step = time_step
            self.sim_time += time_step

            if mass_flow == 0:
                return TimeStepSimulationResponse(outlet_temp=inlet_temp, heat_rate=0)

            self.my_bh.set_flow_rate(mass_flow / self.NUM_BH)
            self.bh_resist = self.my_bh.resist_bh_ave

            self.load_aggregation.get_new_current_load_bin(width=time_step)
            self.load_aggregation.current_load.g = self.get_g_func(time_step)
            self.temp_rise_history = self.calc_temp_rise_history()

            flow_change_frac = abs((mass_flow - self.prev_mass_flow_rate) / mass_flow)

            if flow_change_frac > self.flow_change_fraction_limit:
                self.time_of_prev_flow = self.time_of_curr_flow
                self.time_of_curr_flow = self.sim_time
                self.prev_flow_frac = self.flow_fraction
                self.prev_mass_flow_rate = mass_flow

            self.soil_resist = self.calc_soil_resist()
            self.flow_fraction = self.calc_flow_fraction()
            self.ground_temp = self.my_ground_temp(time=self.sim_time, depth=self.my_bh.DEPTH)
            self.fluid_cap = mass_flow * self.fluid.specific_heat

        temp_rise_prev_bin, g_func_prev_bin = self.calc_prev_bin_temp_rise()
        c_1 = (1 - self.flow_fraction) * self.TOT_LENGTH / self.fluid_cap

        load_num = self.ground_temp - inlet_temp + self.temp_rise_history - temp_rise_prev_bin
        load_den = -self.c_0 * g_func_prev_bin - self.bh_resist - c_1

        self.load_per_meter = load_num / load_den
        energy_per_meter = self.load_per_meter * self.time_step

        self.load_aggregation.set_current_load(load=energy_per_meter)

        temp_rise_history = self.calc_current_temp_rise_history()
        self.ave_fluid_temp = self.ground_temp + temp_rise_history + self.load_per_meter * self.bh_resist

        self.curr_total_load = self.load_per_meter * self.TOT_LENGTH
        self.outlet_temp = self.calc_outlet_temp()

        if converged:
            self.load_aggregation.aggregate()
            self.load_aggregation.update_time()
            self.update_g_values()
            self.prev_sim_time = self.sim_time
            self.fluid.update_properties(mean([inlet_temp, self.outlet_temp]))

        return TimeStepSimulationResponse(heat_rate=self.curr_total_load, outlet_temp=self.outlet_temp)

    def calc_outlet_temp(self):

        return self.ave_fluid_temp - self.flow_fraction * self.curr_total_load / self.fluid_cap

        # transit_time = self.my_bh.fluid_volume / self.my_bh.vol_flow_rate
        #
        # # if self.sim_time - self.time_of_prev_flow < 2 * transit_time:
        #
        # LoadData = namedtuple('LoadData', ['energy', 'width', 'f'])
        #
        # def my_hanby(time):
        #     return hanby(time, self.my_bh.vol_flow_rate, self.my_bh.fluid_volume)
        #
        # outlet_temp_calc_vals = []
        #
        # curr = self.load_aggregation.current_load
        # curr_load = curr.energy
        # curr_width = curr.width
        # curr_f = my_hanby(curr_width)
        #
        # outlet_temp_calc_vals.append(LoadData(curr_load, curr_width, curr_f))
        #
        # time = curr_width
        #
        # for load in self.load_aggregation.loads:
        #     if time < 2 * transit_time:
        #         time += load.width
        #         outlet_temp_calc_vals.append(LoadData(load.energy, load.width, my_hanby(time)))
        #     else:
        #         break
        #
        # sum_energy_f = 0
        # sum_width = 0
        # sum_f = 0
        # for data in outlet_temp_calc_vals:
        #     sum_energy_f += data.energy * data.f
        #     sum_width += data.width
        #     sum_f += data.f
        #
        # outlet_temp_load = sum_energy_f / sum_width * self.TOT_LENGTH
        #
        # return self.ave_fluid_temp - self.flow_fraction * outlet_temp_load / self.fluid_cap

        # else:
        #     return self.ave_fluid_temp - self.flow_fraction * self.curr_total_load / self.fluid_cap

    def calc_flow_fraction(self):
        """
        Computes the flow fraction based on the method outlined in:

        Beier, R.A., M.S. Mitchell, J.D. Spitler, S. Javed. 2018. 'Validation of borehole heat
        exchanger models against multi-flow rate thermal response tests.' Geothermics 71, 55-68.

        :return flow fraction
        """

        # Define base variables
        t_i = self.sim_time
        t_i_minus_1 = self.time_of_prev_flow
        cf = self.fluid.specific_heat * self.fluid.density
        cs = self.soil.specific_heat * self.soil.density
        v_f = self.my_bh.FLUID_VOL
        w = self.my_bh.vol_flow_rate
        l_bh = self.my_bh.DEPTH  # noqa: E741
        r_b = self.my_bh.RADIUS
        k_s = self.soil.conductivity

        # Transit time
        t_tr = v_f / w
        self.transit_time = t_tr

        # Equation 3a
        if t_i - t_i_minus_1 <= 0.02 * t_tr:
            return self.prev_flow_frac  # pragma: no cover

        # total internal borehole resistance
        resist_a = self.my_bh.calc_bh_total_internal_resistance()

        # borehole resistance
        resist_b = self.my_bh.resist_bh_ave
        resist_b1 = resist_b * 2

        # Equation 9
        cd_num = v_f * cf
        cd_den = 2 * PI * l_bh * cs * r_b ** 2
        cd = cd_num / cd_den

        # Equation 10
        resist_db = 2 * PI * k_s * resist_b

        psi = cd * exp(2 * resist_db)
        phi = log(psi)

        # Equations 11
        if 0.2 < psi <= 1.2:
            tdsf_over_cd = -8.0554 * phi ** 3 + 3.8111 * phi ** 2 - 3.2585 * phi + 2.8004  # pragma: no cover
        elif 1.2 < phi <= 160:
            tdsf_over_cd = -0.2662 * phi ** 4 + 3.5589 * phi ** 3 - 18.311 * phi ** 2 + 57.93 * phi - 6.1661
        elif 160 < phi <= 2E5:  # pragma: no cover
            tdsf_over_cd = 12.506 * phi + 45.051  # pragma: no cover
        else:
            raise ValueError  # pragma: no cover

        # Equation 12
        t_sf_num = tdsf_over_cd * cf * v_f
        t_sf_den = 2 * PI * l_bh * k_s
        t_sf = t_sf_num / t_sf_den + t_i_minus_1

        resist_s1 = self.soil_resist

        # Equation A.11
        n_a = l_bh / (w * cf * resist_a)

        # Equation A.12, A.13
        n_s1 = l_bh / (w * cf * (resist_b1 + resist_s1))

        # Equation A.5
        a_1 = (sqrt(4 * ((n_a + n_s1) ** 2 - n_a ** 2))) / 2

        # Equation A.6
        a_2 = -a_1

        # Equation A.7
        c_1 = (n_s1 + a_2) * exp(a_2) / (((n_s1 + a_2) * exp(a_2)) - ((n_s1 + a_1) * exp(a_1)))

        # Equation A.8
        c_2 = 1 - c_1

        # Equation A.9
        c_3 = c_1 * (n_s1 + n_a + a_1) / n_a

        # Equation A.10
        c_4 = c_2 * (n_s1 + n_a + a_2) / n_a

        # Equation A.15
        c_5 = c_1 * (1 + (n_a + n_s1 + a_1) / n_a) * (exp(a_1) - 1) / a_1

        # Equation A.16
        c_6 = (1 - c_1) * (1 + (n_a + n_s1 + a_2) / n_a) * (exp(a_2) - 1) / a_2

        # Equation 5
        f_sf = (0.5 * (c_5 + c_6) - (c_3 + c_4)) / (1 - (c_3 + c_4))

        f_old = self.prev_flow_frac

        # Equations 3b and 3c
        if 0.02 * t_tr <= t_i - t_i_minus_1 < t_sf:
            _part_1 = (f_sf - f_old) / 2
            log_num = log((t_i - t_i_minus_1) / (0.02 * t_tr))
            log_den = log(t_sf / (0.02 * t_tr))
            _part_2 = 1 + sin(PI * (log_num / log_den - 0.5))
            f = _part_1 * _part_2 + f_old
        else:
            f = f_sf  # pragma: no cover

        self.prev_flow_frac = f

        return f

    def calc_prev_bin_temp_rise(self):

        try:
            prev_bin = self.load_aggregation.get_most_recent_bin()
            delta_t_prev_bin = prev_bin.time
            q_prev_bin = prev_bin.get_load()
            g_func_prev_bin = self.get_g_func(delta_t_prev_bin)
            temp_rise_prev_bin = q_prev_bin * g_func_prev_bin * self.c_0
        except IndexError:
            temp_rise_prev_bin = 0
            g_func_prev_bin = self.get_g_func(60)

        return temp_rise_prev_bin, g_func_prev_bin

    def calc_temp_rise(self, bin_i, bin_i_minus_1):
        load_i = bin_i.get_load()
        load_i_minus_1 = bin_i_minus_1.get_load()
        return (load_i - load_i_minus_1) * bin_i_minus_1.g * self.c_0

    def calc_current_temp_rise_history(self):

        temp_rise_sum = 0

        try:
            bin_i = self.load_aggregation.current_load
            bin_i_minus_1 = self.load_aggregation.loads[0]
            temp_rise_sum += self.calc_temp_rise(bin_i, bin_i_minus_1)
        except IndexError:
            bin_i = self.load_aggregation.current_load
            temp_rise_sum += bin_i.get_load() * bin_i.g * self.c_0

        return self.temp_rise_history + temp_rise_sum

    def calc_temp_rise_history(self):

        temp_rise_sum = 0

        for i in range(len(self.load_aggregation.loads) - 1):
            bin_i = self.load_aggregation.loads[i]
            bin_i_minus_1 = self.load_aggregation.loads[i + 1]
            temp_rise_sum += self.calc_temp_rise(bin_i, bin_i_minus_1)

        try:
            bin_i = self.load_aggregation.loads[-1]
            temp_rise_sum += bin_i.get_load() * bin_i.g * self.c_0
        except IndexError:
            pass

        return temp_rise_sum

    def calc_soil_resist(self):
        part_1 = 2 / (4 * PI * self.soil.conductivity)
        part_2_num = 4 * self.soil.diffusivity * self.sim_time
        if part_2_num == 0:
            self.soil_resist = 0  # pragma: no cover
        else:
            part_2_den = GAMMA * self.bh_resist ** 2
            self.soil_resist = part_1 * log(part_2_num / part_2_den)
            if self.soil_resist < 0:
                self.soil_resist = 0
        return self.soil_resist
