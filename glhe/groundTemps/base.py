from abc import ABC, abstractmethod


class BaseGroundTemp(ABC):

    @abstractmethod
    def get_temp(self, time, depth):
        """
        Abstract getter method for ground temperatures

        :param time: time for ground temperature [s]
        :param depth: depth for ground temperature [m]
        :return:
        """

        pass  # pragma: no cover
