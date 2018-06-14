from abc import ABC, abstractmethod


class Base(ABC):

    @abstractmethod
    def get_value(self, time):
        pass  # pragma: no cover
