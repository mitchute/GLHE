from math import sqrt

from numpy import mean
from scipy.optimize import minimize_scalar

from glhe.globals.functions import merge_dicts
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.interface.entry import SimulationEntryPoint
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.path import Path


class GLHE(SimulationEntryPoint):

    def __init__(self, inputs):

        self.name = inputs["simulation"]["name"]
        self.paths = []

        self.fluid = Fluid(inputs["fluid"])
        self.soil = PropertiesBase(inputs['soil'])

        self.delta_p_path = 100000

        self.ground_temp = make_ground_temperature_model(merge_dicts(inputs['ground-temperature'],
                                                                     {'soil-diffusivity': self.soil.diffusivity}
                                                                     )).get_temp

        init_temp = self.ground_temp(0, 100)

        self.inlet_temp = init_temp
        self.outlet_temp = init_temp

        for path in inputs["paths"]:
            self.paths.append(Path(merge_dicts(path, {'initial temp': init_temp}),
                                   fluid_inst=self.fluid, soil_inst=self.soil))

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
