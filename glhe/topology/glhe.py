from math import sqrt

from glhe.properties.fluid import Fluid
from glhe.topology.path import Path

from scipy.optimize import minimize
from numpy import array


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
        path_flow_resistance = []
        for path in self._paths:
            path_flow_resistance.append(path.get_flow_resistance())

        self._delta_p_path = minimize(self.calc_total_mass_flow_from_delta_p, x0=array([self._delta_p_path]),
                                      args=(path_flow_resistance, plant_mass_flow_rate), method='Nelder-Mead',
                                      options={"maxiter": 10}).x[0]

        for i, path in enumerate(self._paths):
            path.set_mass_flow_rate(sqrt(self._delta_p_path / path_flow_resistance[i]))

    def calc_total_mass_flow_from_delta_p(self, delta_p, path_flow_resistance, plant_mass_flow_rate):
        path_mass_flow = []
        for i, _ in enumerate(self._paths):
            path_mass_flow.append(sqrt(delta_p / path_flow_resistance[i]))
        return abs(plant_mass_flow_rate - sum(path_mass_flow))

    def simulate(self, plant_inlet_temperature, plant_mass_flow_rate, curr_simulation_time):
        self.set_flow_rates(plant_mass_flow_rate)
        pass
