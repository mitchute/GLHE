from glhe.groundTemps.base import BaseGroundTemp


class SingleHarmonic(BaseGroundTemp):

    """
    Single harmonic ground temperature model.

    Kusuda, T., and P. R. Achenbach. 1965. Earth temperatures and thermal diffusivity at selected
    stations in the United States. ASHRAE Transactions 71(1): 61-74.
    """

    def __init__(self, ave_temp, amplitude, phase_shift):

        """
        Constructor parameters:

        :param ave_temp:
        :param amplitude:
        :param phase_shift:
        """

        self._ave_ground_temp = ave_temp
        self._amplitude = amplitude
        self._phase_shift = phase_shift
