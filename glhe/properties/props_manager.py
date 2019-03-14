from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid


class PropsMGR(object):

    def __init__(self):
        self.fluid = None
        self.soil = None

    def load_properties(self, inputs: dict) -> None:
        for _, key in enumerate(inputs):
            if key == 'fluid':
                self._add_fluid_props_inst(inputs[key])
            elif key == 'soil':
                self._add_soil_props_inst(inputs[key])

    def _add_fluid_props_inst(self, inputs):
        self.fluid = Fluid(inputs)

    def _add_soil_props_inst(self, inputs):
        self.soil = PropertiesBase(inputs)
