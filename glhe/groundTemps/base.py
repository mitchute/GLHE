from abc import ABC, abstractmethod


class BaseGroundTemp(ABC):

    @abstractmethod
    def get_temp(self, time, depth):
        pass  # pragma: no cover
