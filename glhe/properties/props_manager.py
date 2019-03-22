from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid


class PropsMGR(object):

    def __init__(self):
        self.fluid = None
        self.soil = None

    def load_properties(self, inputs: dict) -> None:
        """
        Load all global properties

        :param inputs: input dictionary
        """
        for key in inputs:
            if key == 'fluid':
                self._add_fluid_props_inst(inputs[key])
            elif key == 'soil':
                self._add_soil_props_inst(inputs[key])

    def _add_fluid_props_inst(self, inputs: dict) -> None:
        """
        Inits the fluid properties class

        :param inputs: fluid input dict
        """
        self.fluid = Fluid(inputs)

    def _add_soil_props_inst(self, inputs: dict) -> None:
        """
        Inits the soil properties class

        :param inputs: soil input dict
        """
        self.soil = PropertiesBase(inputs)
