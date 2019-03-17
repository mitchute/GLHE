from abc import ABC, abstractmethod


class BaseLoad(ABC):

    @abstractmethod
    def get_value(self, time):
        pass  # pragma: no cover
