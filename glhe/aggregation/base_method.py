from abc import ABC, abstractmethod
from collections import deque


class BaseMethod(ABC):

    def __init__(self):
        self.current_load = None
        self.loads = deque()
        self.type = None

    def update_time(self):
        time = 0
        for load in self.loads:
            if load.g_fixed:
                break  # pragma: no cover
            time += load.width
            load.time = time

    def set_current_load(self, load):
        self.current_load.energy = load

    def get_most_recent_bin(self):
        try:
            return self.loads[0]
        except IndexError:
            raise IndexError

    def aggregate_current_load(self):
        self.loads.appendleft(self.current_load)

    @abstractmethod
    def get_new_current_load_bin(self):
        pass  # pragma: no cover

    @abstractmethod
    def aggregate(self):
        pass  # pragma: no cover
