from math import sqrt

from numpy import mean
from scipy.optimize import minimize_scalar

from glhe.interface.entry import SimulationEntryPoint
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.path import Path


class GLHE(SimulationEntryPoint):
    count = 0

    def __init__(self, inputs):

        # Get inputs from json blob

        self.name = inputs["simulation"]["name"]
        self.paths = []

        # Fluid instance
        self.fluid = Fluid(inputs["fluid"])
        self.soil = PropertiesBase(inputs['soil'])

        # Initialize other parameters
        self.delta_p_path = 100000
        self.inlet_temp = 20
        self.outlet_temp = 20

        # Initialize all paths; pass fluid instance for later usage
        for path in inputs["paths"]:
            self.paths.append(Path(path, fluid=self.fluid, soil=self.soil))

        # Track GLHE num
        self.glhe_num = GLHE.count
        GLHE.count += 1

    def set_flow_rates(self, plant_mass_flow_rate):
        for path in self.paths:
            path.set_flow_resistance()

        self.delta_p_path = minimize_scalar(self.calc_total_mass_flow_from_delta_p, args=plant_mass_flow_rate,
                                            method='Golden', bracket=(0, self.delta_p_path), bounds=(0, 10e7),
                                            tol=0.01).x

        for i, path in enumerate(self.paths):
            path.set_mass_flow_rate(sqrt(self.delta_p_path / path.flow_resistance))

    def calc_total_mass_flow_from_delta_p(self, delta_p, plant_mass_flow_rate):
        path_mass_flow = []
        for i, path in enumerate(self.paths):
            path_mass_flow.append(sqrt(delta_p / path.flow_resistance))
        return abs(plant_mass_flow_rate - sum(path_mass_flow))

    def simulate_time_step(self, plant_inlet_temperature, plant_mass_flow_rate, curr_simulation_time):
        self.inlet_temp = plant_inlet_temperature
        self.fluid.update_properties(mean([self.inlet_temp, self.outlet_temp]))
        self.set_flow_rates(plant_mass_flow_rate)

        for path in self.paths:
            path.simulate(self.inlet_temp)
