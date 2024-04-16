from __future__ import annotations

from scp.ethyl_alcohol import EthylAlcohol
from scp.ethylene_glycol import EthyleneGlycol
from scp.methyl_alcohol import MethylAlcohol
from scp.propylene_glycol import PropyleneGlycol
from scp.water import Water


class Fluid:
    def __init__(self, inputs: dict):
        self.type = inputs['fluid-type'].upper()
        if self.type == "WATER":
            concentration = 0
            self.fluid = Water()
        elif self.type == "EA":
            concentration = inputs['concentration'] / 100.0
            self.fluid = EthylAlcohol(concentration)
        elif self.type == "EG":
            concentration = inputs['concentration'] / 100.0
            self.fluid = EthyleneGlycol(concentration)
        elif self.type == "MA":
            concentration = inputs['concentration'] / 100.0
            self.fluid = MethylAlcohol(concentration)
        elif self.type == "PG":
            concentration = inputs['concentration'] / 100.0
            self.fluid = PropyleneGlycol(concentration)
        else:
            raise ValueError("Fluid '{}' fluid is not valid.".format(self.type))

        self.min_temp = self.fluid.t_min
        self.max_temp = self.fluid.t_max

    def get_cp(self, temperature: int | float) -> float:
        """
        Computes the fluid specific heat

        :param temperature: temperature, in Celsius
        :returns fluid specific heat in [J/kg-K]
        """

        return self.fluid.specific_heat(temperature)

    def get_k(self, temperature: int | float) -> float:
        """
        Computes the fluid conductivity

        :param temperature: temperature, in Celsius
        :return: fluid conductivity in [W/m-K]
        """

        return self.fluid.conductivity(temperature)

    def get_mu(self, temperature: int | float) -> float:
        """
        Computes the fluid viscosity

        :param temperature: temperature, in Celsius
        :return: fluid viscosity in [Pa-s]
        """

        return self.fluid.viscosity(temperature)

    def get_pr(self, temperature: int | float) -> float:
        """
        Computes the fluid Prandtl number

        :param temperature: temperature, in Celsius
        :return: fluid Prandtl number
        """

        return self.fluid.prandtl(temperature)

    def get_rho(self, temperature: int | float) -> float:
        """
        Computes the fluid density

        :param temperature: temperature, in Celsius
        :return: fluid density in [kg/m^3]
        """

        return self.fluid.density(temperature)

    def get_rho_cp(self, temperature: int | float) -> float:
        """
        Computes the fluid volume-specific heat capacity

        :param temperature: temperature, in Celsius
        :return: fluid volume-specific heat capacity in [J/m3-K]
        """

        return self.fluid.density(temperature) * self.fluid.specific_heat(temperature)
