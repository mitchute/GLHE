from math import cos, exp, pi, sqrt

from glhe.ground_temps.base import BaseGroundTemp
from glhe.utilities.constants import SEC_IN_YEAR


class SingleHarmonic(BaseGroundTemp):
    """
    Single harmonic ground temperature model.

    Kusuda, T., and P. R. Achenbach. 1965. Earth temperatures and thermal diffusivity at selected
    stations in the United States. ASHRAE Transactions 71(1): 61-74.
    """

    def __init__(self, inputs: dict):
        self.ave_ground_temp = inputs['average-temperature']
        self.amplitude = inputs['amplitude']
        self.phase_shift = inputs['phase-shift']
        self.soil_diffusivity = inputs['soil-diffusivity']

    def get_temp(self, time: int, depth: float) -> float:
        term1 = -depth * sqrt(pi / (SEC_IN_YEAR * self.soil_diffusivity))
        c = (2 * pi / SEC_IN_YEAR)
        term2 = c * (time - self.phase_shift - (depth / 2) * sqrt(SEC_IN_YEAR / (pi * self.soil_diffusivity)))
        return self.ave_ground_temp - self.amplitude * exp(term1) * cos(term2)
