from numpy import genfromtxt
from scipy.interpolate import interp1d

from glhe.aggregation.factory import load_agg_factory
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.properties.base import PropertiesBase


class GFunction(SimulationEntryPoint):
    def __init__(self, inputs):
        self.inputs = inputs

        # g-function properties
        g_functions = genfromtxt(inputs['g-functions']['file'], delimiter=',')
        self.g_function = interp1d(g_functions[:, 0], g_functions[:, 1], fill_value='extrapolate')
        self.average_depth = inputs['g-functions']['average-depth']
        self.soil = PropertiesBase(
            conductivity=inputs['soil']['conductivity'],
            density=inputs['soil']['density'],
            specific_heat=inputs['soil']['specific heat']
        )

        # initialize time here
        self.current_time = 0
        self.load_aggregation = load_agg_factory(inputs['load-aggregation'])

    def simulate_time_step(self, inlet_temperature, flow, time_step):
        self.current_time += time_step
        outlet_temperature = inlet_temperature
        # calculate total heat transfer
        # self.load_aggregation.store_load(q)
        # a = self._agg.loads[0].get_load()  # save load to history
        return TimeStepSimulationResponse(outlet_temperature=outlet_temperature)
