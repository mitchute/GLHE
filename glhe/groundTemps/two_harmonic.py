from math import cos, exp, sqrt, pi

from glhe.groundTemps.base import BaseGroundTemp

from glhe.globals.constants import SEC_IN_DAY, DAYS_IN_YEAR


class TwoHarmonic(BaseGroundTemp):
    """
    Two harmonic ground temperature model.

    Xing, L. and J. D. Spitler. 2017. Prediction of undisturbed ground temperature using analytical and numerical modeling.
    Part I: Model development and experimental validation. Science and Technology for the Built Environment 23(5): 787-808.

    Xing, L. and J. D. Spitler. 2017. Prediction of undisturbed ground temperature using analytical and numerical modeling.
    Part II: Methodology for developing a world-wide dataset. Science and Technology for the Built Environment 23(5): 809-825.

    Xing, L., J. D. Spitler and A. Bandyopadhyay. 2017. Prediction of undisturbed ground temperature using analytical and numerical modeling.
    Part III: Experimental validation of a world-wide dataset. Science and Technology for the Built Environment 23(5): 826-842.
    """

    def __init__(self, ave_temp, amplitude_1, amplitude_2, phase_shift_1, phase_shift_2, soil_diffusivity):
        """
        Constructor parameters:

        :param ave_temp: Average temperature of the soil [C]
        :param amplitude_1: First soil surface temperature amplitude [C]
        :param amplitude_2: Second soil surface temperature amplitude parameter [C]
        :param phase_shift_1: Phase shift of surface temperature amplitude 1 [days]
        :param phase_shift_2: Phase shift of surface temperature amplitude 2 [days]
        :param soil_diffusivity: Soil thermal diffusivity [m2/s]
        """

        self._ave_ground_temp = ave_temp
        self._amplitude_1 = amplitude_1
        self._amplitude_2 = amplitude_2
        self._phase_shift_1 = phase_shift_1
        self._phase_shift_2 = phase_shift_2
        self._soil_diffusivity = soil_diffusivity

    def get_temp(self, time, depth):

        time_in_days = time / SEC_IN_DAY

        n = 1
        term1 = -depth * sqrt((n * pi) / (self._soil_diffusivity * DAYS_IN_YEAR))
        term2 = (2 * pi * n) / DAYS_IN_YEAR * (time_in_days - self._phase_shift_1) \
                - depth * sqrt((n * pi) / (self._soil_diffusivity * DAYS_IN_YEAR))

        n = 2
        term3 = -depth * sqrt((n * pi) / (self._soil_diffusivity * DAYS_IN_YEAR))
        term4 = (2 * pi * n) / DAYS_IN_YEAR * (time_in_days - self._phase_shift_2) \
                - depth * sqrt((n * pi) / (self._soil_diffusivity * DAYS_IN_YEAR))

        summation = exp(term1) * self._amplitude_1 * cos(term2) + exp(term3) * self._amplitude_2 * cos(term4)

        return self._ave_ground_temp - summation
