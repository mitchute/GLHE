from glhe.ground_temps.ground_temp_factory import make_ground_temp_model
from glhe.properties.base_properties import PropertiesBase
from glhe.properties.fluid_properties import Fluid


class PropsMGR(object):

    def __init__(self):
        self.fluid = None
        self.soil = None

    def load_properties(self, inputs: dict) -> None:
        # TODO: pull this into the init structure

        """
        Load all global properties

        :param inputs: input dictionary
        """

        # load properties first
        for key in inputs:
            if key == 'fluid':
                self._add_fluid_props_inst(inputs[key])
            elif key == 'soil':
                self._add_soil_props_inst(inputs[key])

        # tack ground temp model onto the soil class
        for key in inputs:
            if key == 'ground-temperature-model':
                self._add_ground_temperature_model(inputs[key])

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

    def _add_ground_temperature_model(self, inputs: dict) -> None:
        """
        Inits the ground temperature model

        :param inputs: ground temp model inputs dict
        """
        gtm_cls = make_ground_temp_model(inputs)
        self.soil.get_temp = gtm_cls.get_temp
