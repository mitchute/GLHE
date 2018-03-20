from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, conductivity=0, density=0, specific_heat=0, inner_diameter=0, outer_diameter=0):
        PropertiesBase.__init__(self, conductivity=conductivity, density=density, specific_heat=specific_heat)
        self._inner_diameter = inner_diameter
        self._outer_diameter = outer_diameter
        self._thickness = (self._outer_diameter - self._inner_diameter) / 2.0
