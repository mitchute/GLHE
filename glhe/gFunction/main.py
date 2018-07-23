from math import log, exp

from numpy import genfromtxt, mean
from scipy.interpolate import interp1d

from glhe.aggregation.factory import load_agg_factory
from glhe.globals.constants import PI
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.outputProcessor.processor import OutputProcessor
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
        self.prev_mass_flow_rate = 0

    def get_g_func(self, time):
        """
        Retrieves the interpolated g-function value

        :param time: time [s]
        :return: g-function value
        """

        lntts = log(time / self.t_s)
        return self._g_function_interp(lntts)

    def simulate_time_step(self, inlet_temperature, mass_flow, time_step):
        op = OutputProcessor()
        self.current_time += time_step
        fluid_cap = mass_flow * self.fluid.specific_heat
        if mass_flow == 0:
            return TimeStepSimulationResponse(outlet_temperature=inlet_temperature, heat_rate=0)
        else:
            ground_temp = self.my_ground_temp(time=self.current_time, depth=self.my_bh.depth)

            if self.prev_mass_flow_rate != mass_flow:
                self.my_bh.mass_flow_rate = mass_flow / self.num_bh
                self.prev_mass_flow_rate = mass_flow
                self.bh_resist = self.my_bh.calc_bh_resistance()
                op.register_output_variable(self, 'bh_resist', "Borehole Resistance [K/(W/m)]")

                self.flow_fraction = self.calc_flow_fraction()
                op.register_output_variable(self, 'flow_fraction', "Flow Fraction [-]")

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
            op.register_output_variable(self, 'load_normalized', "Load on GHE [W/m]")

            total_load = self.load_normalized * self.tot_length

            energy = self.load_normalized * time_step

            self.load_aggregation.add_load(load=energy, width=time_step, time=self.current_time)

            self.ave_fluid_temp = inlet_temperature - (1 - self.flow_fraction) * total_load / fluid_cap
            op.register_output_variable(self, 'ave_fluid_temp', "Average Fluid Temp [C]")

            outlet_temperature = self.ave_fluid_temp - self.flow_fraction * total_load / fluid_cap

            # update for next time step
            self.fluid.update_properties(mean([inlet_temperature, outlet_temperature]))

            return TimeStepSimulationResponse(heat_rate=total_load, outlet_temperature=outlet_temperature)

    def calc_flow_fraction(self):
        fluid_vol_heat_capacity = self.fluid.specific_heat * self.fluid.density
        soil_vol_heat_capacity = self.soil.specific_heat * self.soil.density
        volume = self.my_bh.fluid_volume

        fluid_storage_coefficient_num = volume * fluid_vol_heat_capacity
        fluid_storage_coefficient_den = 2 * PI * self.my_bh.depth * soil_vol_heat_capacity * self.my_bh.radius ** 2

        fluid_storage_coefficient = fluid_storage_coefficient_num / fluid_storage_coefficient_den

        resist_bh_dimensionless = 2 * PI * self.soil.conductivity * self.my_bh.resist_bh

        psi = fluid_storage_coefficient * exp(2 * resist_bh_dimensionless)
        phi = log(psi)

        if 0.2 < psi <= 1.2:
            td_over_cd = -8.0554 * phi ** 3 + 3.8111 * phi ** 2 - 3.2585 * phi + 2.8004
        elif 1.2 < phi <= 160:
            td_over_cd = -0.2662 * phi ** 4 + 3.5589 * phi ** 3 - 18.311 * phi ** 2 + 57.93 * phi - 6.1661
        elif 160 < phi <= 2E5:
            td_over_cd = 12.506 * phi + 45.051
        else:
            raise ValueError

        steady_flux_time_num = td_over_cd * fluid_vol_heat_capacity * volume
        steady_flux_time_den = 2 * PI * self.my_bh.depth * self.soil.conductivity

        steady_flux_time = steady_flux_time_num / steady_flux_time_den

        flow_factor = (0.5 * (c_5 + c_6) - (c_3 + c_4)) / (1 - (c_3 + c_4))

        return 0.5

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
