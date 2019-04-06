from abc import ABC, abstractmethod

import numpy as np


class BaseMethod(ABC):

    def __init__(self):
        self.loads = np.empty((0,), dtype=float)
        self.times = np.empty((0,), dtype=int)
        self.dts = np.empty((0,), dtype=int)
        self.g_vals = np.empty((0,), dtype=float)
        self.prev_update_time = 0

    @abstractmethod
    def aggregate(self, time: int, energy: float):
        pass  # pragma: no cover
