from math import log, exp, sqrt, sin

from numpy import genfromtxt, mean
from scipy.interpolate import interp1d

from glhe.aggregation.factory import load_agg_factory
from glhe.globals.constants import PI, GAMMA
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.outputProcessor.processor import op
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.borehole import Borehole


class GFunction(SimulationEntryPoint):
    def __init__(self, inputs):
        self.inputs = inputs

        # g-function properties
        g_functions = genfromtxt(inputs['g-functions']['file'], delimiter=',')

        self._g_function_interp = interp1d(g_functions[:, 0],
                                           g_functions[:, 1],
                                           fill_value='extrapolate')

        self.fluid = Fluid(inputs['fluid'])
        self.soil = PropertiesBase(inputs=inputs['soil'])

        # initialize time here
        self.current_time = 0

        # init load aggregation method
        self.load_aggregation = load_agg_factory(inputs['load-aggregation'])
        self.load_aggregation.add_load(load=0, width=0, time=0)

        # response constant
        self.c_0 = 1 / (2 * PI * self.soil.conductivity)

        # ground temperature model
        ground_temp_model_inputs = inputs['ground-temperature']
        ground_temp_model_inputs['soil-diffusivity'] = self.soil.diffusivity
        self.my_ground_temp = make_ground_temperature_model(ground_temp_model_inputs).get_temp

        self.my_bh = Borehole(inputs['g-functions']['borehole-data'], self.fluid, self.soil)
        self.num_bh = inputs['g-functions']['number of boreholes']

        self.tot_length = self.my_bh.depth * self.num_bh

        # time constant
        self.t_s = self.my_bh.depth ** 2 / (9 * self.soil.diffusivity)

        # other inits
        self.bh_resist = 0
        self.ave_fluid_temp = 0
        self.flow_fraction = 0
        self.load_normalized = 0
        self.prev_mass_flow_rate = -999
        self.prev_flow_frac = 0
        self.time_of_curr_flow = 0
        self.time_of_prev_flow = 0
        self.flow_change_fraction_limit = 0.1

    def register_output_variables(self):
        op.register_output_variable(self, 'bh_resist', "Borehole Resistance [K/(W/m)]")
        op.register_output_variable(self, 'flow_fraction', "Flow Fraction [-]")
        op.register_output_variable(self, 'load_normalized', "Load on GHE [W/m]")
        op.register_output_variable(self, 'ave_fluid_temp', "Average Fluid Temp [C]")

    def get_g_func(self, time):
        """
        Retrieves the interpolated g-function value

        :param time: time [s]
        :return: g-function value
        """

        lntts = log(time / self.t_s)
        g = self._g_function_interp(lntts)

        if (g / (2 * PI * self.soil.conductivity) + self.my_bh.resist_bh) < 0:
            return -self.my_bh.resist_bh * 2 * PI * self.soil.conductivity
        else:
            return g

    def simulate_time_step(self, inlet_temperature, mass_flow, time_step):
        self.current_time += time_step

        if self.prev_mass_flow_rate != mass_flow:
            self.time_of_prev_flow = self.time_of_curr_flow
            self.time_of_curr_flow = self.current_time

        if mass_flow == 0:
            return TimeStepSimulationResponse(outlet_temperature=inlet_temperature, heat_rate=0)

        if self.prev_mass_flow_rate != mass_flow:
            self.my_bh.set_flow_rate(mass_flow / self.num_bh)
            self.bh_resist = self.my_bh.calc_bh_resistance()

            flow_change_frac = abs((mass_flow - self.prev_mass_flow_rate) / mass_flow)

            if flow_change_frac > self.flow_change_fraction_limit:
                self.prev_flow_frac = self.flow_fraction

            self.prev_mass_flow_rate = mass_flow

        ground_temp = self.my_ground_temp(time=self.current_time, depth=self.my_bh.depth)
        fluid_cap = mass_flow * self.fluid.specific_heat
        self.flow_fraction = self.calc_flow_fraction()

        prev_bin = self.load_aggregation.loads[0]
        delta_t_prev_bin = self.current_time - prev_bin.abs_time
        q_prev_bin = prev_bin.get_load()
        g_func_prev_bin = self.get_g_func(delta_t_prev_bin)

        temp_rise_prev_bin = q_prev_bin * g_func_prev_bin * self.c_0

        temp_rise_history = self.calc_history_temp_rise()

        c_1 = (1 - self.flow_fraction) * self.tot_length / fluid_cap

        load_num = ground_temp - inlet_temperature + temp_rise_history - temp_rise_prev_bin
        load_den = -self.c_0 * g_func_prev_bin - self.bh_resist - c_1
        self.load_normalized = load_num / load_den

        total_load = self.load_normalized * self.tot_length

        energy_normalized = self.load_normalized * time_step

        self.load_aggregation.add_load(load=energy_normalized, width=time_step, time=self.current_time)

        # self.ave_fluid_temp = inlet_temperature - (1 - self.flow_fraction) * total_load / fluid_cap
        self.ave_fluid_temp = ground_temp +  self.calc_history_temp_rise() + self.load_normalized * self.bh_resist

        t_out_fict = inlet_temperature - total_load / fluid_cap

        self.ave_fluid_temp = mean([t_out_fict, inlet_temperature])

        outlet_temperature = self.ave_fluid_temp - self.flow_fraction * total_load / fluid_cap

        # update for next time step
        self.fluid.update_properties(mean([inlet_temperature, outlet_temperature]))

        return TimeStepSimulationResponse(heat_rate=total_load, outlet_temperature=outlet_temperature)

    def calc_flow_fraction(self):
        """
            Computes the flow fraction based on the method outlined in:

            Beier, R.A., M.S. Mitchell, J.D. Spitler, S. Javed. 2018. 'Validation of borehole heat
            exchanger models against multi-flow rate thermal response tests.' Geothermics 71, 55-68.

            :return flow fraction
            """

        # Define base variables
        t_i = self.current_time
        t_i_minus_1 = self.time_of_prev_flow
        cf = self.fluid.specific_heat * self.fluid.density
        cs = self.soil.specific_heat * self.soil.density
        v_f = self.my_bh.fluid_volume
        w = self.my_bh.vol_flow_rate
        l = self.my_bh.depth  # noqa: E741
        r_b = self.my_bh.radius
        k_s = self.soil.conductivity

        # Transit time
        t_tr = v_f / w

        # Equation 3a
        if t_i - t_i_minus_1 <= 0.02 * t_tr:
            return self.prev_flow_frac

        # total internal borehole resistance
        resist_a = self.my_bh.resist_bh_total_internal

        # borehole resistance
        resist_b = self.my_bh.resist_bh_ave
        resist_b1 = resist_b / 2
        resist_b2 = resist_b / 2

        # Equation 9
        cd_num = v_f * cf
        cd_den = 2 * PI * l * cs * r_b ** 2
        cd = cd_num / cd_den

        # Equation 10
        resist_db = 2 * PI * k_s * resist_b

        psi = cd * exp(2 * resist_db)
        phi = log(psi)

        # Equations 11
        if 0.2 < psi <= 1.2:
            tdsf_over_cd = -8.0554 * phi ** 3 + 3.8111 * phi ** 2 - 3.2585 * phi + 2.8004
        elif 1.2 < phi <= 160:
            tdsf_over_cd = -0.2662 * phi ** 4 + 3.5589 * phi ** 3 - 18.311 * phi ** 2 + 57.93 * phi - 6.1661
        elif 160 < phi <= 2E5:
            tdsf_over_cd = 12.506 * phi + 45.051
        else:
            raise ValueError

        # Equation 12
        t_sf_num = tdsf_over_cd * cf * v_f
        t_sf_den = 2 * PI * l * k_s
        t_sf = t_sf_num / t_sf_den + t_i_minus_1

        # soil resistance
        resist_s = 1 / (4 * PI * k_s) * log(4 * self.soil.diffusivity * (t_sf + t_i_minus_1) / (GAMMA * r_b ** 2))
        resist_s1 = resist_s * 2
        resist_s2 = resist_s * 2

        # Equation A.11
        n_a = l / (w * cf * resist_a)

        # Equation A.12
        n_s1 = l / (w * cf * (resist_b1 + resist_s1))

        # Equation A.13
        n_s2 = l / (w * cf * (resist_b2 + resist_s2))

        # Equation A.5
        a_1 = (-(n_s1 - n_s2) + sqrt((n_s1 - n_s2) ** 2 + 4 * ((n_a + n_s1) * (n_a + n_s2) - n_a ** 2))) / 2

        # Equation A.6
        a_2 = (-(n_s1 - n_s2) - sqrt((n_s1 - n_s2) ** 2 + 4 * ((n_a + n_s1) * (n_a + n_s2) - n_a ** 2))) / 2

        # Equation A.7
        c_1 = (n_s1 + a_2) * exp(a_2) / (((n_s1 + a_2) * exp(a_2)) - ((n_s1 + a_1) * exp(a_1)))

        # Equation A.8
        c_2 = 1 - c_1

        # Equation A.9
        c_3 = c_1 * (n_s1 + n_a + a_1) / n_a

        # Equation A.10
        c_4 = c_2 * (n_s1 + n_a + a_2) / n_a

        # Equation A.15
        c_5 = c_1 * (1 + n_s2 / n_s1 * (n_a + n_s1 + a_1) / n_a) * (exp(a_1) - 1) / a_1

        # Equation A.16
        c_6 = (1 - c_1) * (1 + n_s2 / n_s1 * (n_a + n_s1 + a_2) / n_a) * (exp(a_2) - 1) / a_2

        # Equation 5
        f_sf = (0.5 * (c_5 + c_6) - (c_3 + c_4)) / (1 - (c_3 + c_4))

        f_old = self.prev_flow_frac

        # Equations 3b and 3c
        if 0.02 * t_tr <= t_i - t_i_minus_1 < t_sf:
            _part_1 = (f_sf - f_old) / 2
            _part_2 = sin(PI * log((t_i - t_i_minus_1) / (0.02 * t_tr) / log(t_sf / (0.02 * t_tr)) - 0.5))
            return _part_1 * (1 + _part_2) + f_old
        else:
            return f_sf

    def calc_history_temp_rise(self):
        length = len(self.load_aggregation.loads)

        temp_rise_sum = 0
        try:
            for i in range(length - 1):
                # this occurred nearer to the current sim time
                bin_i = self.load_aggregation.loads[i]

                # this occurred farther from the current sim time
                bin_i_minus_1 = self.load_aggregation.loads[i + 1]

                g_func_val = self.get_g_func(self.current_time - bin_i_minus_1.abs_time)

                load_i = bin_i.get_load()
                load_i_minus_1 = bin_i_minus_1.get_load()

                temp_rise_sum += (load_i - load_i_minus_1) * g_func_val * self.c_0
        except IndexError:
            pass

        return temp_rise_sum