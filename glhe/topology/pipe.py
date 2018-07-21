from math import factorial, exp

from numpy import log

from glhe.globals.constants import PI
from glhe.globals.functions import smoothing_function
from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, inputs, fluid):
        PropertiesBase.__init__(self, inputs=inputs)
        self.inner_diameter = inputs["inner diameter"]
        self.outer_diameter = inputs["outer diameter"]
        self.thickness = (self.outer_diameter - self.inner_diameter) / 2
        self.inner_radius = self.inner_diameter / 2
        self.outer_radius = self.outer_diameter / 2

        self._fluid = fluid

        self.friction_factor = 0.02
        self.resist_pipe = 0

    def calc_friction_factor(self, re):
        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        lower_limit = 1500
        upper_limit = 5000

        if re < lower_limit:
            self.friction_factor = self.laminar_friction_factor(re)
        elif lower_limit <= re < upper_limit:
            f_low = self.laminar_friction_factor(re)
            # pure turbulent flow
            f_high = self.turbulent_friction_factor(re)
            sigma = smoothing_function(re, a=3000, b=450)
            self.friction_factor = (1 - sigma) * f_low + sigma * f_high
        else:
            self.friction_factor = self.turbulent_friction_factor(re)

        return self.friction_factor

    def calc_conduction_resistance(self):
        """
        Calculates the thermal resistance of a pipe, in [K/(W/m)].

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        return log(self.outer_diameter / self.inner_diameter) / (2 * PI * self.conductivity)

    def calc_convection_resistance(self, mass_flow_rate):
        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        lower_limit = 2000
        upper_limit = 4000

        re = 4 * mass_flow_rate / (self._fluid.viscosity * PI * self.inner_diameter)

        if re < lower_limit:
            nu = self._laminar_nusselt()
        elif lower_limit <= re < upper_limit:
            nu_low = self._laminar_nusselt()
            nu_high = self._turbulent_nusselt(re)
            sigma = smoothing_function(re, a=3000, b=150)
            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            nu = self._turbulent_nusselt(re)
        return 1 / (nu * PI * self._fluid.conductivity)

    def calc_resistance(self, mass_flow_rate):
        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 3
        """

        self.resist_pipe = self.calc_convection_resistance(mass_flow_rate) + self.calc_conduction_resistance()
        return self.resist_pipe

    @staticmethod
    def _laminar_nusselt():
        """
        Laminar Nusselt number for smooth pipes

        mean(4.36, 3.66)
        :return: Nusselt number
        """
        return 4.01

    def _turbulent_nusselt(self, re):
        """
        Turbulent Nusselt number for smooth pipes

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.

        :param re: Reynolds number
        :return: Nusselt number
        """

        f = self.calc_friction_factor(re)
        pr = self._fluid.prandtl
        return (f / 8) * (re - 1000) * pr / (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))

    @staticmethod
    def laminar_friction_factor(re):
        """
        Laminar friction factor

        :param re: Reynolds number
        :return: friction factor
        """

        return 64.0 / re

    @staticmethod
    def turbulent_friction_factor(re):
        """

        :param re:
        :return:
        """

        return (0.79 * log(re) - 1.64) ** (-2.0)

    @staticmethod
    def hanby(time, vol_flow_rate, volume):
        """
        Computes the non-dimensional response of a fluid conduit
        assuming well mixed nodes. The model accounts for the thermal
        capacity of the fluid and diffusive mixing.

        Hanby, V.I., J.A. Wright, D.W. Fetcher, D.N.T. Jones. 2002
        'Modeling the dynamic response of conduits.' HVAC&R Research 8(1): 1-12.

        The model is non-dimensional, so input parameters should have consistent units
        for that are able to compute the non-dimensional time parameter, tau.

        :math \tau = \frac{\dot{V} \cdot t}{Vol}


        :param time: time of fluid response
        :param vol_flow_rate: volume flow rate
        :param volume: volume of fluid circuit
        :return:
        """

        tau = vol_flow_rate * time / volume
        num_nodes = 20
        ret_sum = 1
        for i in range(1, num_nodes):
            ret_sum += (num_nodes * tau) ** i / factorial(i)

        return 1 - exp(-num_nodes * tau) * ret_sum
