class PropertiesBase(object):

    def __init__(self, conductivity=0, density=0, specific_heat=0):
        self.conductivity = conductivity
        self.density = density
        self.specific_heat = specific_heat
        self.diffusivity = self._diffusivity()

    def _diffusivity(self):
        return self.conductivity / (self.specific_heat * self.density)
