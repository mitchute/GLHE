from glhe.topology.path import Path
from glhe.properties.fluid import Fluid


class GLHE(object):

    _count = 0

    def __init__(self, inputs):

        # Get inputs from json blob
        self._name = inputs["name"]
        self._paths = []

        self._glhe_num = GLHE._count
        GLHE._count += 1

        # Fluid instance
        self._fluid = Fluid(inputs["fluid"])

        # Initialize all paths
        for path in inputs["paths"]:
            self._paths.append(Path(path, fluid_instance=self._fluid))

        # initialize flow distribution based on constants in delta p calculation
        path_const_flow_resist = []
        for path in self._paths:
            path_const_flow_resist.append(0)
            path_const_flow_resist[-1] += path.const_flow_resistance

        tot_const_flow_resistance = sum(path_const_flow_resist)
        for path in self._paths:
            path.mass_flow_fraction = path.const_flow_resistance / tot_const_flow_resistance

    def set_flow_rates(self, plant_mass_flow_rate):
        path_delta_p = []
        for path in self._paths:
            path_delta_p.append(1 / path.flow_resistance(path.mass_flow_fraction * plant_mass_flow_rate))

        delta_p_tot = pow(sum(path_delta_p), -1)

        for i, path in enumerate(self._paths):
            path.set_flow_rate(path_delta_p[i] / delta_p_tot, path.mass_flow_fraction * plant_mass_flow_rate)

    def simulate(self, plant_inlet_temperature, plant_mass_flow_rate, curr_simulation_time):
        self.set_flow_rates(plant_mass_flow_rate)
        pass
