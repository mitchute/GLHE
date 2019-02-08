from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid


class PropsMGR(object):
    grout = []
    fluid = []
    soil = []

    def __init__(self):
        pass

    @classmethod
    def add_grout_props_inst(cls, inputs):
        cls.grout.append(PropertiesBase(inputs))

    @classmethod
    def add_fluid_props_inst(cls, inputs):
        cls.fluid.append(Fluid(inputs))

    @classmethod
    def add_soil_props_inst(cls, inputs):
        cls.fluid.append(Fluid(inputs))

    @staticmethod
    def _get_idx(lst, err_msg, name):
        for idx, inst in enumerate(lst):
            if inst.name == name:
                return idx
            else:
                raise ValueError(err_msg)

    def get_grout_props_idx(self, name):
        return self._get_idx(PropsMGR.grout, 'Grout properties not found', name)

    def get_fluid_props_idx(self, name):
        return self._get_idx(PropsMGR.fluid, 'Fluid properties not found', name)

    def get_soil_props_idx(self, name):
        return self._get_idx(PropsMGR.soil, 'Soil properties not found', name)
