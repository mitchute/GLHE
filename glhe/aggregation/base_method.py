from abc import ABC, abstractmethod
from collections import deque


class BaseMethod(ABC):

    def __init__(self):
        self.loads = deque()
        self.type = None

    def update_time(self):
        time = 0
        for load in self.loads:
            time += load.width
            load.time = time

    def set_current_load(self, load):
        self.loads[0].energy = load

    def reset_current_load(self):
        self.loads[0].energy = 0

    def get_most_recent_bin(self):
        try:
            return self.loads[1]
        except IndexError:
            return self.loads[0]

    @abstractmethod
    def add_load(self, bin_width, sim_time):
        pass  # pragma: no cover

    @abstractmethod
    def aggregate(self, sim_time):
        pass  # pragma: no cover
