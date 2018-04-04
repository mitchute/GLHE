from math import sqrt

from glhe.properties.fluid import Fluid
from glhe.topology.path import Path

from scipy.optimize import minimize_scalar
from numpy import array, nan


class GLHE(object):

    _count = 0

    def __init__(self, inputs):

        # Get inputs from json blob
        self._name = inputs["name"]
        self._paths = []

        # Fluid instance
        self._fluid = Fluid(inputs["fluid"])

        # Initialize other parameters
        self._delta_p_path = 100000

        # Initialize all paths; pass fluid instance for later usage
        for path in inputs["paths"]:
            self._paths.append(Path(path, fluid_instance=self._fluid))

        # Track GLHE num
        self._glhe_num = GLHE._count
        GLHE._count += 1

    def set_flow_rates(self, plant_mass_flow_rate):
        for path in self._paths:
            path.set_flow_resistance()

        self._delta_p_path = minimize_scalar(self.calc_total_mass_flow_from_delta_p, args=plant_mass_flow_rate,
                                             method='Golden', bracket=(0, self._delta_p_path), bounds=(0, 10e7),
                                             tol=0.01).x

        for i, path in enumerate(self._paths):
            path.set_mass_flow_rate(sqrt(self._delta_p_path / path.flow_resistance))

    def calc_total_mass_flow_from_delta_p(self, delta_p, plant_mass_flow_rate):
        path_mass_flow = []
        for i, path in enumerate(self._paths):
            path_mass_flow.append(sqrt(delta_p / path.flow_resistance))
        return abs(plant_mass_flow_rate - sum(path_mass_flow))

    def simulate(self, plant_inlet_temperature, plant_mass_flow_rate, curr_simulation_time):
        self.set_flow_rates(plant_mass_flow_rate)
        pass
