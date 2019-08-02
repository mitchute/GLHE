class PropertiesBase(object):

    def __init__(self, inputs):

        if 'name' in inputs:
            if hasattr(self, 'name'):
                pass
            else:
                self.name = inputs['name']

        self.conductivity = inputs["conductivity"]
        self.density = inputs["density"]
        self.specific_heat = inputs["specific-heat"]
        self.heat_capacity = self.calc_rho_cp()
        self.diffusivity = self.calc_alpha()

    def calc_rho_cp(self):
        return self.density * self.specific_heat

    def calc_alpha(self):
        return self.conductivity / (self.specific_heat * self.density)
