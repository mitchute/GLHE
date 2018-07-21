from glhe.groundTemps.base import BaseGroundTemp


class Constant(BaseGroundTemp):
    """
    Constant ground temperature model.
    """

    def __init__(self, temp):
        """
        Constructor parameters:

        :param temp: Temperature of the soil [C]
        """

        self._temp = temp

    def get_temp(self, time=None, depth=None):
        """
        Constant ground temperature

        :return: ground temperature [C]
        """

        return self._temp
