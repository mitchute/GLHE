class PropertiesBase(object):

    def __init__(self, inputs):
        self.conductivity = inputs["conductivity"]
        self.density = inputs["density"]
        self.specific_heat = inputs["specific heat"]
        self.diffusivity = self._diffusivity()

    def _diffusivity(self):
        return self.conductivity / (self.specific_heat * self.density)
