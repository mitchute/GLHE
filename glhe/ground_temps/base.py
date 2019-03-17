from abc import ABC, abstractmethod


class BaseGroundTemp(ABC):
    """
    Abstract base class for ground temperature objects
    """

    @abstractmethod
    def get_temp(self, time, depth):
        """
         Getter method for ground temperatures

        :param time: time for ground temperature [s]
        :param depth: depth for ground temperature [m]
        :return: ground temperature [C]
        """
        pass  # pragma: no cover
