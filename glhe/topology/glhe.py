from glhe.topology.path import Path


class GLHE(object):

    _count = 0

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._paths = []

        self._glhe_num = GLHE._count
        GLHE._count += 1

        for path in inputs["paths"]:
            self._paths.append(Path(path))

        self._fluid = inputs["fluid"]

    def set_path_flow_rates(self, plant_mass_flow_rate):
        for path in self._paths:
            path.flow_resistance()

    def simulate(self, inlet_temperature, plant_mass_flow_rate, simulation_time):
        self.set_path_flow_rates(plant_mass_flow_rate)
        pass
