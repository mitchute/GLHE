from CoolProp.CoolProp import PropsSI

from glhe.globals.functions import temp_in_kelvin
from glhe.properties.fluid_property_types import FluidPropertyType
from glhe.properties.fluid_types import FluidType


class Fluid(object):
    pressure = 120000
    specific_heat = 0
    density = 0
    conductivity = 0
    prandtl = 0
    viscosity = 0
    temperature = 0

    def __init__(self, inputs):
        self._fluid_name = inputs["type"].upper()

        if self._fluid_name == "WATER":
            self._fluid_type = FluidType.WATER
        elif self._fluid_name == "EA":
            self._fluid_type = FluidType.ETHYL_ALCOHOL
            self._concentration = inputs["concentration"] / 100.0
        elif self._fluid_name == "EG":
            self._fluid_type = FluidType.ETHYLENE_GLYCOL
            self._concentration = inputs["concentration"] / 100.0
        elif self._fluid_name == "PG":
            self._fluid_type = FluidType.PROPYLENE_GLYCOL
            self._concentration = inputs["concentration"] / 100.0
        else:
            raise ValueError("'{}' fluid is not supported".format(self._fluid_name))

        self._min_temperature = -200
        self._max_temperature = 200
        self._min_concentration = 0
        self._max_concentration = 100

        # Fluid definitions: http://www.coolprop.org/fluid_properties/Incompressibles.html#the-different-fluids
        if self._fluid_type == FluidType.WATER:
            self._fluid_str = "WATER"
            self._min_temperature = 0
            self._max_temperature = 200
        elif self._fluid_type == FluidType.ETHYL_ALCOHOL:
            self._fluid_str = "INCOMP::MEA[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 40
            self._min_concentration = 0
            self._max_concentration = 60
        elif self._fluid_type == FluidType.ETHYLENE_GLYCOL:
            self._fluid_str = "INCOMP::MEG[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 100
            self._min_concentration = 0
            self._max_concentration = 60
        elif self._fluid_type == FluidType.PROPYLENE_GLYCOL:
            self._fluid_str = "INCOMP::MPG[{0}]".format(self._concentration)
            self._min_temperature = -100
            self._max_temperature = 100
            self._min_concentration = 0
            self._max_concentration = 60

        self.temp_freeze = self.calc_freezing_point()

        # init at 20 C
        self.update_properties(20)

    def update_properties(self, temperature):
        Fluid.temperature = temperature
        Fluid.conductivity = self.calc_conductivity(temperature)
        Fluid.specific_heat = self.calc_specific_heat(temperature)
        Fluid.density = self.calc_density(temperature)
        Fluid.prandtl = self.calc_prandtl(temperature)
        Fluid.viscosity = self.calc_viscosity(temperature)

    def calc_freezing_point(self):
        """
        Determines the freezing point of the fluid.
        Uses the CoolProp python library.

        :returns fluid freezing point in [K]
        """

        if self._fluid_type == FluidType.WATER:
            return 273.15
        else:
            return PropsSI("T_FREEZE", self._fluid_str)

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

    def _calc_property(self, property, temperature):
        """
        Worker function to call the CoolProp library

        :param property: Fluid property enum value
        :param temperature: Fluid temperature in Celsius
        :return: Property Value
        """

        props = {FluidPropertyType.CONDUCTIVITY: 'CONDUCTIVITY',
                 FluidPropertyType.DENSITY: 'D',
                 FluidPropertyType.PRANDTL: 'PRANDTL',
                 FluidPropertyType.SPECIFIC_HEAT: 'C',
                 FluidPropertyType.VISCOSITY: 'VISCOSITY'}

        try:
            return PropsSI(props[property],
                           'T', temp_in_kelvin(temperature),
                           'P', self.pressure,
                           self._fluid_str)
        except ValueError:
            print("Temperature out of range. Fluid properties evaluated at the freezing point.")
            return PropsSI(props[property],
                           'T', self.temp_freeze,
                           'P', self.pressure,
                           self._fluid_str)
