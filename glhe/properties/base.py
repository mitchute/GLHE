class PropertiesBase(object):

    def __init__(self, conductivity=0, density=0, specific_heat=0):
        self._conductivity = conductivity
        self._density = density
        self._specific_heat = specific_heat

    def diffusivity(self):
        return self._conductivity / (self._specific_heat * self._density)
