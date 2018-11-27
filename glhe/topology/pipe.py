from numpy import log, ones

from glhe.globals.constants import PI
from glhe.globals.functions import smoothing_function
from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, inputs, fluid):
        PropertiesBase.__init__(self, inputs=inputs)
        self.INNER_DIAMETER = inputs["inner diameter"]
        self.OUTER_DIAMETER = inputs["outer diameter"]
        self.LENGTH = inputs['length']

        self.THICKNESS = (self.OUTER_DIAMETER - self.INNER_DIAMETER) / 2
        self.INNER_RADIUS = self.INNER_DIAMETER / 2
        self.OUTER_RADIUS = self.OUTER_DIAMETER / 2

        self.AREA_CR_INNER = PI / 4 * self.INNER_DIAMETER ** 2
        self.FLUID_VOL = self.AREA_CR_INNER * self.LENGTH

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
        LOWER_LIMIT = 1500
        UPPER_LIMIT = 5000

        if re < LOWER_LIMIT:
            self.friction_factor = self.laminar_friction_factor(re)
        elif LOWER_LIMIT <= re < UPPER_LIMIT:
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

        return log(self.OUTER_DIAMETER / self.INNER_DIAMETER) / (2 * PI * self.conductivity)

    def calc_convection_resistance(self, mass_flow_rate):
        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        LOWER_LIMIT = 2000
        UPPER_LIMIT = 4000

        re = 4 * mass_flow_rate / (self._fluid.viscosity * PI * self.INNER_DIAMETER)

        if re < LOWER_LIMIT:
            nu = self.laminar_nusselt()
        elif LOWER_LIMIT <= re < UPPER_LIMIT:
            nu_low = self.laminar_nusselt()
            nu_high = self.turbulent_nusselt(re)
            sigma = smoothing_function(re, a=3000, b=150)
            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            nu = self.turbulent_nusselt(re)
        return 1 / (nu * PI * self._fluid.conductivity)

    def set_resistance(self, pipe_resistance):
        self.resist_pipe = pipe_resistance
        return self.resist_pipe

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
    def laminar_nusselt():
        """
        Laminar Nusselt number for smooth pipes

        mean(4.36, 3.66)
        :return: Nusselt number
        """
        return 4.01

    def turbulent_nusselt(self, re):
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
