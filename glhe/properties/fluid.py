from CoolProp.CoolProp import PropsSI

from glhe.topology.fluid_types import FluidType


class Fluid(object):
    pressure = 120000
    specific_heat = 0
    density = 0
    conductivity = 0
    prandtl = 0
    viscosity = 0

    def __init__(self, inputs):
        self._fluid_name = inputs["type"].upper()

        if self._fluid_name == "WATER":
            self._type = FluidType.WATER
        elif self._fluid_name == "EA":
            self._type = FluidType.ETHYL_ALCOHOL
            self._concentration = inputs["concentration"] / 100.0
        elif self._fluid_name == "EG":
            self._type = FluidType.ETHYLENE_GLYCOL
            self._concentration = inputs["concentration"] / 100.0
        elif self._fluid_name == "PG":
            self._type = FluidType.PROPYLENE_GLYCOL
            self._concentration = inputs["concentration"] / 100.0
        else:
            raise ValueError("'{}' is not supported".format(self._fluid_name))

        self._min_temperature = -200
        self._max_temperature = 200
        self._min_concentration = 0
        self._max_concentration = 100

        # Fluid definitions: http://www.coolprop.org/fluid_properties/Incompressibles.html#the-different-fluids
        if self._type == FluidType.WATER:
            self._props_str = "WATER"
            self._min_temperature = 0
            self._max_temperature = 200
        elif self._type == FluidType.ETHYL_ALCOHOL:
            self._props_str = "INCOMP::MEA[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 40
            self._min_concentration = 0
            self._max_concentration = 60
        elif self._type == FluidType.ETHYLENE_GLYCOL:
            self._props_str = "INCOMP::MEG[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 100
            self._min_concentration = 0
            self._max_concentration = 60
        elif self._type == FluidType.PROPYLENE_GLYCOL:
            self._props_str = "INCOMP::MPG[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 100
            self._min_concentration = 0
            self._max_concentration = 60

        # init at 20 C
        self.update(20)

    def update(self, temperature):
        Fluid.conductivity = self.calc_cond(temperature)
        Fluid.specific_heat = self.calc_cp(temperature)
        Fluid.density = self.calc_dens(temperature)
        Fluid.prandtl = self.calc_pr(temperature)
        Fluid.viscosity = self.calc_visc(temperature)

    def calc_cond(self, temperature):
        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid conductivity in [W/m-K]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('CONDUCTIVITY', 'T', temp_in_kelvin, 'P', self.pressure, self._props_str)

    def calc_cp(self, temperature):
        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.

        :returns fluid specific heat in [J/kg-K]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('C', 'T', temp_in_kelvin, 'P', self.pressure, self._props_str)

    def calc_dens(self, temperature):
        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid density in [kg/m3]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('D', 'T', temp_in_kelvin, 'P', self.pressure, self._props_str)

    def calc_pr(self, temperature):
        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid Prandtl number
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('PRANDTL', 'T', temp_in_kelvin, 'P', self.pressure, self._props_str)

    def calc_visc(self, temperature):
        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid viscosity in [Pa-s]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('VISCOSITY', 'T', temp_in_kelvin, 'P', self.pressure, self._props_str)
