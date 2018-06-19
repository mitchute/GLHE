from numpy import log, exp

from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, inputs, fluid):
        PropertiesBase.__init__(self, conductivity=inputs["pipe"]["conductivity"],
                                density=inputs["pipe"]["density"],
                                specific_heat=inputs["pipe"]["specific heat"])
        self.inner_diameter = inputs["pipe"]["inner diameter"]
        self.outer_diameter = inputs["pipe"]["outer diameter"]
        self.thickness = (self.outer_diameter - self.inner_diameter) / 2
        self.inner_radius = self.inner_diameter / 2
        self.outer_radius = self.outer_diameter / 2

        self._fluid = fluid

        self.friction_factor = 0.02

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
            self.friction_factor = 64.0 / re  # pure laminar flow
        elif lower_limit <= re < upper_limit:
            f_low = 64.0 / re  # pure laminar flow
            # pure turbulent flow
            f_high = (0.79 * log(re) - 1.64) ** (-2.0)
            sf = 1 / (1 + exp(-(re - 3000.0) / 450.0))  # smoothing function
            self.friction_factor = (1 - sf) * f_low + sf * f_high
        else:
            self.friction_factor = (0.79 * log(re) - 1.64) ** (-2.0)  # pure turbulent flow

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
            nu = 4.01  # laminar mean(4.36, 3.66)
        elif lower_limit <= re < upper_limit:
            nu_low = 4.01  # laminar
            f = self.calc_friction_factor(re)  # turbulent
            pr = self._fluid.prandtl
            nu_high = (f / 8) * (re - 1000) * pr / \
                      (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))
            sigma = 1 / (1 + exp(-(re - 3000) / 150))  # smoothing function

            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            f = self.calc_friction_factor(re)
            pr = self._fluid.prandtl
            nu = (f / 8) * (re - 1000) * pr / \
                 (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))

        h = nu * self._fluid.conductivity / self.inner_diameter
        return 1 / (h * PI * self.inner_diameter)

    def calc_resistance(self, mass_flow_rate):
        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 3
        """

        return self.calc_convection_resistance(mass_flow_rate) + self.calc_conduction_resistance()
