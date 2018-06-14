import csv

from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.properties.base import PropertiesBase


class GFunction(SimulationEntryPoint):
    def __init__(self, inputs):
        self.inputs = inputs

        # g-function properties
        g_functions = []
        with(open(inputs['g-functions']['file'])) as f:
            csv_file = csv.reader(f)
            for row in csv_file:
                g_functions.append((row[0], row[1]))
        self.g_functions = g_functions
        self.average_depth = inputs['g-functions']['average-depth']

        # soil properties
        soil = PropertiesBase(
            conductivity=inputs['soil']['conductivity'],
            density=inputs['soil']['density'],
            specific_heat=inputs['soil']['specific heat']
        )
        self.soil_diffusivity = soil.diffusivity()

        # initialize time here
        self.current_time = 0
        # self.load_aggregation = load_agg_factory()

    def _get_g_function(self, time):
        pass

    def simulate_time_step(self, inlet_temperature, flow, time_step):
        self.current_time += time_step
        outlet_temperature = inlet_temperature
        # calculate total heat transfer
        # self.load_aggregation.store_load(q)
        # a = self._agg.loads[0].get_load()  # save load to history
        return TimeStepSimulationResponse(outlet_temperature=outlet_temperature)
