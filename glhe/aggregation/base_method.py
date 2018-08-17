from abc import ABC, abstractmethod
from collections import deque


class BaseMethod(ABC):

    def __init__(self):
        self.loads = deque()
        self.last_time = 0

    @abstractmethod
    def add_load(self, load, time):
        pass  # pragma: no cover

    @abstractmethod
    def update_aggregation(self, time):
        pass  # pragma: no cover

    @abstractmethod
    def aggregate(self):
        pass  # pragma: no cover

    @abstractmethod
    def get_most_recent_bin(self):
        pass  # pragma: no cover

    def reset_to_prev(self):
        self.last_time -= self.loads[0].width
        self.loads.popleft()
