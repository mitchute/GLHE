import csv

from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse
from glhe.properties.base import PropertiesBase
from glhe.aggregation.factory import load_agg_factory


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
        self.soil = PropertiesBase(
            conductivity=inputs['soil']['conductivity'],
            density=inputs['soil']['density'],
            specific_heat=inputs['soil']['specific heat']
        )

        # initialize time here
        self.current_time = 0
        self.load_aggregation = load_agg_factory(inputs['load-aggregation'])

    def get_g_function(self, time):
        # don't cover this until it's actually implemented
        pass  # pragma: no cover

    def interp_g_function(self, non_dimensional_time):
        """
        Interpolate logarithmically for g-function value

        Malayappan, V. and J.D. Spitler. 2013. Limitations of Using Uniform Heat Flux Assumptions in
        Sizing Vertical Borehole Heat Exchanger Fields. Proceedings of Clima 2013. June 16-19. Prague.

        :param non_dimensional_time: the non-dimensional time t/ts to which the g-functions are mapped
        :return: g-function value
        """

        

        return 0

    def simulate_time_step(self, inlet_temperature, flow, time_step):
        self.current_time += time_step
        outlet_temperature = inlet_temperature
        # calculate total heat transfer
        # self.load_aggregation.store_load(q)
        # a = self._agg.loads[0].get_load()  # save load to history
        return TimeStepSimulationResponse(outlet_temperature=outlet_temperature)
