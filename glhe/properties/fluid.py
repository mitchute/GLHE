from glhe.topology.fluid_types import FluidType

from CoolProp.CoolProp import PropsSI


class Fluid(object):

    _pressure = 120000

    def __init__(self, fluid_name, concentration=0):
        self._fluid_name = fluid_name.upper()
        self._concentration = concentration / 100

        if self._fluid_name == "WATER":
            self._type = FluidType.WATER
        elif self._fluid_name == "EA":
            self._type = FluidType.ETHYL_ALCOHOL
        elif self._fluid_name == "EG":
            self._type = FluidType.ETHYLENE_GLYCOL
        elif self._fluid_name == "PG":
            self._type = FluidType.PROPYLENE_GLYCOL
        else:
            self._type = fluid_name

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
        else:
            self._props_str = fluid_name

    def cp(self, temperature):
        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.

        :returns fluid specific heat in [J/kg-K]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('C', 'T', temp_in_kelvin, 'P', self._pressure, self._props_str)

    def dens(self, temperature):
        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid density in [kg/m3]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('D', 'T', temp_in_kelvin, 'P', self._pressure, self._props_str)

    def visc(self, temperature):
        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid viscosity in [Pa-s]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('VISCOSITY', 'T', temp_in_kelvin, 'P', self._pressure, self._props_str)

    def cond(self, temperature):
        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid conductivity in [W/m-K]
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('CONDUCTIVITY', 'T', temp_in_kelvin, 'P', self._pressure, self._props_str)

    def pr(self, temperature):
        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid Prandtl number
        """

        temp_in_kelvin = temperature + 273.15
        return PropsSI('PRANDTL', 'T', temp_in_kelvin, 'P', self._pressure, self._props_str)
