from math import cos, exp, pi, sqrt

from glhe.globals.constants import DAYS_IN_YEAR, SEC_IN_DAY
from glhe.ground_temps.base import BaseGroundTemp


class TwoHarmonic(BaseGroundTemp):
    """
    Two harmonic ground temperature model.

    Xing, L. and J. D. Spitler. 2017. 'Prediction of undisturbed ground temperature using analytical
    and numerical modeling. Part I: Model development and experimental validation.'
    Science and Technology for the Built Environment 23(5): 787-808.

    Xing, L. and J. D. Spitler. 2017. 'Prediction of undisturbed ground temperature using analytical
    and numerical modeling. Part II: Methodology for developing a world-wide dataset.'
     Science and Technology for the Built Environment 23(5): 809-825.

    Xing, L., J. D. Spitler and A. Bandyopadhyay. 2017. 'Prediction of undisturbed ground temperature
    using analytical and numerical modeling. Part III: Experimental validation of a world-wide dataset.'
    Science and Technology for the Built Environment 23(5): 826-842.
    """

    def __init__(self, inputs: dict):
        self.ave_ground_temp = inputs['average-temperature']
        self.amplitude_1 = inputs['amplitude-1']
        self.amplitude_2 = inputs['amplitude-2']
        self.phase_shift_1 = inputs['phase-shift-1']
        self.phase_shift_2 = inputs['phase-shift-2']
        self.soil_diffusivity = inputs['soil-diffusivity']

    def get_temp(self, time: int, depth: float) -> float:
        term1 = self._exp_term(n=1, depth=depth)
        term2 = self._cos_term(n=1, time=time, depth=depth)
        term3 = self._exp_term(n=2, depth=depth)
        term4 = self._cos_term(n=2, time=time, depth=depth)
        summation = exp(term1) * self.amplitude_1 * cos(term2) + exp(term3) * self.amplitude_2 * cos(term4)
        return self.ave_ground_temp - summation

    def _exp_term(self, n: int, depth: float) -> float:
        return -depth * sqrt((n * pi) / (self.soil_diffusivity * DAYS_IN_YEAR))

    def _cos_term(self, n: int, time: int, depth: float) -> float:
        time_in_days = time / SEC_IN_DAY
        term_2_pt_1 = (2 * pi * n) / DAYS_IN_YEAR * (time_in_days - self.phase_shift_1)
        term_2_pt_2 = depth * sqrt((n * pi) / (self.soil_diffusivity * DAYS_IN_YEAR))
        return term_2_pt_1 - term_2_pt_2
