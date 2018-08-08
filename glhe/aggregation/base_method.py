from abc import ABC, abstractmethod

from collections import deque


class BaseMethod(ABC):

    def __init__(self):
        self.loads = deque()

    @abstractmethod
    def add_load(self, load, time):
        pass  # pragma: no cover

    @abstractmethod
    def reset_to_prev(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_delta_q(self, current_time):
        pass  # pragma: no cover
