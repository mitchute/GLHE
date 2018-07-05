from math import log

from numpy import genfromtxt
from scipy.interpolate import interp1d

from glhe.aggregation.factory import load_agg_factory
from glhe.globals.constants import PI
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.properties.base import PropertiesBase

from glhe.topology.borehole import Borehole


class GFunction(SimulationEntryPoint):
    def __init__(self, inputs):
        self.inputs = inputs

        # g-function properties
        g_functions = genfromtxt(inputs['g-functions']['file'],
                                 delimiter=',')

        self._g_function = interp1d(g_functions[:, 0],
                                    g_functions[:, 1], 
                                    fill_value='extrapolate')

        self.average_depth = inputs['g-functions']['average-depth']

        self.soil = PropertiesBase(
            conductivity=inputs['soil']['conductivity'],
            density=inputs['soil']['density'],
            specific_heat=inputs['soil']['specific heat'])

        # initialize time here
        self.current_time = 0

        # init load aggregation method
        self.load_aggregation = load_agg_factory(inputs['load-aggregation'])

        # time constant
        self.t_s = self.average_depth ** 2 / (9 * self.soil.diffusivity)

        # response constant
        self.c_0 = 1 / (2 * PI * self.soil.conductivity)

        # ground temperature model
        gtm_inputs = inputs['ground-temperature']
        gtm_inputs['soil-diffusivity'] = self.soil.diffusivity
        self.my_ground_temp = make_ground_temperature_model(gtm_inputs).get_temp

        # init borehole
        bh_inputs = inputs


    def get_g_func(self, time):
        """
        Retrieves the interpolated g-function value

        :param time: time [s]
        :return: g-function value
        """

        lntts = log(time / self.t_s)
        return self._g_function(lntts)

    def simulate_time_step(self, inlet_temperature, flow, time_step):
        self.current_time += time_step
        heat_rate = 0
        outlet_temperature = inlet_temperature
        if flow >= 0:
            ground_temp = self.my_ground_temp(self.current_time)


        return TimeStepSimulationResponse(outlet_temperature=outlet_temperature, heat_rate=heat_rate)

        # self.load_aggregation.store_load(q)
        # a = self._agg.loads[0].get_load()  # save load to history        return TimeStepSimulationResponse(outlet_temperature=outlet_temperature)

