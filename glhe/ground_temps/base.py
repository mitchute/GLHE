from abc import ABC, abstractmethod


class BaseGroundTemp(ABC):
    """
    Abstract base class for ground temperature objects
    """

    @abstractmethod
    def get_temp(self, time: int, depth: float) -> float:
        """
         Getter method for ground temperatures

        :param time: time for ground temperature [s]  # TODO: Should we use float instead of int for time?
        :param depth: depth for ground temperature [m]
        :return: ground temperature [C]
        """
        pass  # pragma: no cover
