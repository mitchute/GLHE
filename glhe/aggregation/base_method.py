from abc import ABC, abstractmethod

import numpy as np


class BaseMethod(ABC):

    def __init__(self):
        # energy values to be tracked
        self.loads = np.empty((0,), dtype=float)

        # time referenced from current simulation time
        # most recent values appended to array
        self.times = np.empty((0,), dtype=int)

        # time step of each respective bin
        self.dts = np.empty((0,), dtype=int)

        # g-function values for each respective bin
        self.g_vals = np.empty((0,), dtype=float)

        # previous time the aggregation method was updated
        self.prev_update_time = 0

    @abstractmethod
    def aggregate(self, time: int, energy: float):
        pass  # pragma: no cover
