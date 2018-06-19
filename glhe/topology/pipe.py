from numpy import log, exp

from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, conductivity=0, density=0, specific_heat=0, inner_diameter=0, outer_diameter=0):
        PropertiesBase.__init__(self, conductivity=conductivity, density=density, specific_heat=specific_heat)
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.thickness = (self.outer_diameter - self.inner_diameter) / 2
        self.inner_radius = self.inner_diameter / 2
        self.outer_radius = self.outer_diameter / 2

    @staticmethod
    def calc_friction_factor(re):
        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        lower_limit = 1500
        upper_limit = 5000

        if re < lower_limit:
            return 64.0 / re  # pure laminar flow
        elif lower_limit <= re < upper_limit:
            f_low = 64.0 / re  # pure laminar flow
            # pure turbulent flow
            f_high = (0.79 * log(re) - 1.64) ** (-2.0)
            sf = 1 / (1 + exp(-(re - 3000.0) / 450.0))  # smoothing function
            return (1 - sf) * f_low + sf * f_high
        else:
            return (0.79 * log(re) - 1.64) ** (-2.0)  # pure turbulent flow