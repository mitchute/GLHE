from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid


class PropsMGR(object):
    fluid = None
    soil = None

    def __init__(self):
        pass

    @classmethod
    def load_properties(cls, inputs: dict) -> None:
        for _, key in enumerate(inputs):
            if key == 'fluid':
                cls._add_fluid_props_inst(inputs[key])
            elif key == 'soil':
                cls._add_soil_props_inst(inputs[key])

    @classmethod
    def _add_fluid_props_inst(cls, inputs):
        cls.fluid = Fluid(inputs)

    @classmethod
    def _add_soil_props_inst(cls, inputs):
        cls.soil = PropertiesBase(inputs)
