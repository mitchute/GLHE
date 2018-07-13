from math import log

from numpy import genfromtxt
from scipy.interpolate import interp1d

from glhe.aggregation.factory import load_agg_factory
from glhe.globals.constants import PI
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

    def get_g_func(self, time):
        """
        Retrieves the interpolated g-function value

        :param time: time [s]
        :return: g-function value
        """

        lntts = log(time / self.t_s)
        return self._g_function_interp(lntts)

    def simulate_time_step(self, inlet_temperature, flow, time_step):
        self.current_time += time_step
        fluid_cap = flow * self.fluid.specific_heat
        if flow == 0:
            return TimeStepSimulationResponse(outlet_temperature=inlet_temperature, heat_rate=0)
        else:
            ground_temp = self.my_ground_temp(time=self.current_time, depth=self.my_bh.depth)
            self.my_bh.mass_flow_rate = flow
            bh_resist = self.my_bh.calc_bh_resistance()

            prev_bin = self.load_aggregation.loads[0]
            delta_t_prev_bin = self.current_time - prev_bin.abs_time
            q_prev_bin = prev_bin.get_load()
            g_func_prev_bin = self.get_g_func(delta_t_prev_bin)

            temp_rise_prev_bin = q_prev_bin * g_func_prev_bin * self.c_0

            temp_rise_history = self.calc_history_temp_rise()

            flow_fraction = self.calc_flow_frac()

            c_1 = (1 - flow_fraction) * self.tot_length / (fluid_cap)

            load_num = ground_temp - temp_rise_history + temp_rise_prev_bin - inlet_temperature
            load_den = self.c_0 * g_func_prev_bin + bh_resist + c_1
            load = load_num / load_den

            energy = load * time_step

            self.load_aggregation.add_load(load=energy, width=time_step, time=self.current_time)

            ave_temp = (1 - flow_fraction) * load * self.tot_length / (self.tot_length) + inlet_temperature

            outlet_temp = ave_temp - flow_fraction * load / fluid_cap

            load_tot = load * self.tot_length

            return TimeStepSimulationResponse(heat_rate=load_tot, outlet_temperature=outlet_temp)

    def calc_flow_frac(self):
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
