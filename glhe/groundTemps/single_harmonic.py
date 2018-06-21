from math import pi, cos, exp, sqrt

from glhe.globals.constants import SEC_IN_YEAR
from glhe.groundTemps.base import BaseGroundTemp


class SingleHarmonic(BaseGroundTemp):
    """
    Single harmonic ground temperature model.

    .. math::
        a^2 + b^2 = c^2

    Kusuda, T., and P. R. Achenbach. 1965. Earth temperatures and thermal diffusivity at selected
    stations in the United States. ASHRAE Transactions 71(1): 61-74.
    """

    def __init__(self, ave_temp, amplitude, phase_shift, soil_diffusivity):
        """
        Constructor parameters:

        :param ave_temp: Average temperature of the soil [C]
        :param amplitude: Amplitude of the soil temperature variations [C]
        :param phase_shift: Phase shift from first day of year when minimum temperature at the ground surface occurs [days]
        :param soil_diffusivity: Soil thermal diffusivity [m2/s]
        """

        self._ave_ground_temp = ave_temp
        self._amplitude = amplitude
        self._phase_shift = phase_shift
        self._soil_diffusivity = soil_diffusivity

    def get_temp(self, time, depth):
        """
        Computes the ground temperature using the one-harmonic model

        :param time: time [s]
        :param depth: depth below ground surface [m]
        :return: grond temperature [C]
        """

        term_1 = -depth * sqrt(pi / (SEC_IN_YEAR * self._soil_diffusivity))

        term_2_pt_1 = (2 * pi / SEC_IN_YEAR)
        term_2_pt_2 = (time - self._phase_shift - (depth / 2) * sqrt(SEC_IN_YEAR / (pi * self._soil_diffusivity)))
        term_2 = term_2_pt_1 * term_2_pt_2

        return self._ave_ground_temp - self._amplitude * exp(term_1) * cos(term_2)
