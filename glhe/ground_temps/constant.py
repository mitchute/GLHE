from glhe.ground_temps.base import BaseGroundTemp


class Constant(BaseGroundTemp):
    """
    Constant ground temperature model.
    """

    def __init__(self, temp):
        """
        Constructor parameters:

        :param temp: Temperature of the soil [C]
        """

        self.temperature = temp

    def get_temp(self, time=None, depth=None):
        return self.temperature
