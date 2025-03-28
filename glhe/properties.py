
from scp.water import Water

class PropertiesBase:

    def __init__(self, inputs: dict):
        try:
            self.name = inputs['name']
        except KeyError:
            self.name = "Missing"
        self.conductivity = inputs["conductivity"]
        self.density = inputs["density"]
        self.specific_heat = inputs["specific-heat"]
        self.heat_capacity = self.calc_rho_cp()
        self.diffusivity = self.calc_alpha()

    def calc_rho_cp(self) -> float:
        return self.density * self.specific_heat

    def calc_alpha(self) -> float:
        return self.conductivity / (self.specific_heat * self.density)


fluid = Water()

class Soil(PropertiesBase):
    def __init__(self, inputs: dict):
        super().__init__(inputs)
        from glhe.ground_temperature import Constant
        self.get_temp = Constant({'temperature': 10}).get_temp

soil = Soil({
    "name": "dirt",
    "conductivity": 2.7,
    "density": 2500,
    "specific-heat": 880
})