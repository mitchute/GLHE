import os
from abc import ABC, abstractmethod

import numpy as np
from scipy.interpolate import interp1d

join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


class BaseAgg(ABC):

    def __init__(self, inputs):
        # g-function values
        path = norm(join(cwd, inputs['g-function-path']))
        data = np.genfromtxt(path, delimiter=',')
        self.interp_g = interp1d(data[:, 0], data[:, 1], fill_value='extrapolate')
        self.ts = inputs['time-scale']

        # energy values to be tracked
        self.energy = np.empty((0,), dtype=float)

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

    @abstractmethod
    def calc_superposition_coeffs(self, time: int, time_step: int) -> float:
        pass  # pragma: no cover