class PropertiesBase(object):

    def __init__(self, inputs):
        try:
            self.name = inputs['name']
        except KeyError:
            pass
        self.conductivity = inputs["conductivity"]
        self.density = inputs["density"]
        self.specific_heat = inputs["specific-heat"]
        self.vol_heat_capacity = self.vol_heat_capacity()
        self.diffusivity = self.diffusivity()

    def vol_heat_capacity(self):
        return self.density * self.specific_heat

    def diffusivity(self):
        return self.conductivity / (self.specific_heat * self.density)
