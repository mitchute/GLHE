from CoolProp.CoolProp import PropsSI

from glhe.globals.functions import c_to_k
from glhe.properties.fluid_property_types import FluidPropertyType
from glhe.properties.fluid_types import FluidType


class Fluid(object):
    def __init__(self, inputs):
        self.name = inputs['name'].upper()
        self.type = inputs['type'].upper()
        if self.type == "WATER":
            self.fluid_enum = FluidType.WATER
            concentration = 0
        elif self.type == "EA":
            self.fluid_enum = FluidType.ETHYL_ALCOHOL
            concentration = inputs['concentration'] / 100.0
        elif self.type == "EG":
            self.fluid_enum = FluidType.ETHYLENE_GLYCOL
            concentration = inputs['concentration'] / 100.0
        elif self.type == "PG":
            self.fluid_enum = FluidType.PROPYLENE_GLYCOL
            concentration = inputs['concentration'] / 100.0
        else:
            raise ValueError("'{}' fluid is not supported".format(self.type))

        self.fluid_str = self.get_fluid_str(self.fluid_enum, concentration)

        self.min_temp = self.calc_min_temp()
        self.max_temp = self.calc_max_temp()

        self.pressure = 120000
        self.specific_heat = 0
        self.density = 0
        self.conductivity = 0
        self.prandtl = 0
        self.viscosity = 0
        self.heat_capacity = 0
        self.temperature = 0

        # init at 20 C
        self.update_properties(20)

    def update_properties(self, temperature):
        self.temperature = temperature
        self.conductivity = self.calc_conductivity(temperature)
        self.specific_heat = self.calc_specific_heat(temperature)
        self.density = self.calc_density(temperature)
        self.heat_capacity = self.calc_vol_heat_capacity(temperature)
        self.prandtl = self.calc_prandtl(temperature)
        self.viscosity = self.calc_viscosity(temperature)

    @staticmethod
    def get_fluid_str(fluid_enum, concentration):
        # Fluid definitions: http://www.coolprop.org/fluid_properties/Incompressibles.html#the-different-fluids

        def get_concentration(c, min_c, max_c):
            if c < min_c:
                return min_c
            elif c > max_c:
                return max_c
            else:
                return c

        if fluid_enum == FluidType.WATER:
            return "WATER"
        elif fluid_enum == FluidType.ETHYL_ALCOHOL:
            return "INCOMP::MEA[{0}]".format(get_concentration(concentration, 0.0, 0.6))
        elif fluid_enum == FluidType.ETHYLENE_GLYCOL:
            return "INCOMP::MEG[{0}]".format(get_concentration(concentration, 0.0, 0.6))
        elif fluid_enum == FluidType.PROPYLENE_GLYCOL:
            return "INCOMP::MPG[{0}]".format(get_concentration(concentration, 0.0, 0.6))

    def calc_max_temp(self):
        """
        Determines the maximum temperature of the fluid. Not to exceed 100 deg C.

        :return: maximum fluid temperature, in Kelvin
        """

        if self.fluid_enum == FluidType.WATER:
            return c_to_k(100)
        else:
            return PropsSI("T_FREEZE", self.fluid_str)

    def calc_min_temp(self):
        """
        Determines the freezing point of the fluid.

        :returns minimum fluid temperature, in Kelvin
        """

        if self.fluid_enum == FluidType.WATER:
            return PropsSI("T_MIN", self.fluid_str)
        else:
            return PropsSI("T_FREEZE", self.fluid_str)

    def calc_conductivity(self, temperature):
        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid conductivity in [W/m-K]
        """

        return self._calc_property(FluidPropertyType.CONDUCTIVITY, temperature)

    def calc_specific_heat(self, temperature):
        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.

        :returns fluid specific heat in [J/kg-K]
        """

        return self._calc_property(FluidPropertyType.SPECIFIC_HEAT, temperature)

    def calc_density(self, temperature):
        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid density in [kg/m3]
        """

        return self._calc_property(FluidPropertyType.DENSITY, temperature)

    def calc_prandtl(self, temperature):
        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid Prandtl number
        """

        return self._calc_property(FluidPropertyType.PRANDTL, temperature)

    def calc_viscosity(self, temperature):
        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid viscosity in [Pa-s]
        """

        return self._calc_property(FluidPropertyType.VISCOSITY, temperature)

    def calc_vol_heat_capacity(self, temperature):
        """
        Determines the fluid volume-specific heat capacity as a function of temperature, in Celsius.
        Uses the CoolProp python library.

        :returns fluid volume-specific heat capacity in [J/m3-K]
        """

        rho = self._calc_property(FluidPropertyType.DENSITY, temperature)
        cp = self._calc_property(FluidPropertyType.SPECIFIC_HEAT, temperature)

        return rho * cp

    def _calc_property(self, _property, temperature):
        """
        Worker function to call the CoolProp library

        :param _property: Fluid property enum value
        :param temperature: Fluid temperature in Celsius
        :return: Property Value
        """

        props = {FluidPropertyType.CONDUCTIVITY: 'CONDUCTIVITY',
                 FluidPropertyType.DENSITY: 'D',
                 FluidPropertyType.PRANDTL: 'PRANDTL',
                 FluidPropertyType.SPECIFIC_HEAT: 'C',
                 FluidPropertyType.VISCOSITY: 'VISCOSITY'}

        try:
            return PropsSI(props[_property], 'T', c_to_k(temperature), 'P', self.pressure, self.fluid_str)
        except ValueError:  # pragma: no cover
            # remove pragma once CoolProp get's its stuff together regarding supporting current wheels
            # https://github.com/CoolProp/CoolProp/issues/1699
            print("Temperature out of range. Fluid properties evaluated at the freezing point.")
            return PropsSI(props[_property],
                           'T', self.min_temp,
                           'P', self.pressure,
                           self.fluid_str)
