from abc import ABC, abstractmethod

import numpy as np


class BaseMethod(ABC):

    def __init__(self):
        self.loads = np.empty((0,))
        self.times = np.empty((0,))
        self.g_vals = np.empty((0,))
        self.prev_update_time = 0

    @abstractmethod
    def aggregate(self, time, load):
        pass  # pragma: no cover
