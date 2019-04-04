from abc import ABC, abstractmethod

import numpy as np


class BaseMethod(ABC):

    def __init__(self):
        self.loads = np.array(0)
        self.durations = np.array(0)
        self.g_vals = None

    @abstractmethod
    def aggregate(self, time, time_step, load):
        pass  # pragma: no cover
