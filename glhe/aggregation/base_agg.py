import os
from abc import ABC, abstractmethod

import numpy as np
from scipy.interpolate import interp1d

join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


class BaseAgg(ABC):

    def __init__(self, inputs: dict):
        # g-function values
        if 'g-function-path' in inputs:
            path_g = norm(join(cwd, inputs['g-function-path']))
            data_g = np.genfromtxt(path_g, delimiter=',')
        elif 'lntts' and 'g-values' in inputs:
            data_g = np.transpose(np.array([inputs['lntts'], inputs['g-values']]))
        else:
            raise KeyError('g-function data not found.')
        self.interp_g = interp1d(data_g[:, 0], data_g[:, 1], fill_value='extrapolate')

        # g_b-function values
        self.interp_g_b = None
        if 'g_b-function-path' in inputs:
            path_g_b = norm(join(cwd, inputs['g_b-function-path']))
            data_g_b = np.genfromtxt(path_g_b, delimiter=',')
            self.interp_g_b = interp1d(data_g_b[:, 0], data_g_b[:, 1], fill_value='extrapolate')
        elif 'lntts_b' and 'g_b-values' in inputs:
            data_g_b = np.transpose(np.array([inputs['lntts_b'], inputs['g_b-values']]))
            self.interp_g_b = interp1d(data_g_b[:, 0], data_g_b[:, 1], fill_value='extrapolate')

        self.ts = inputs['time-scale']

        # energy values to be tracked
        self.energy = np.empty((0,), dtype=float)

        # most recent values appended to array
        self.times = np.empty((0,), dtype=int)

        # time step of each respective bin
        self.dts = np.empty((0,), dtype=int)

        # previous time the aggregation method was updated
        self.prev_update_time = None

    @abstractmethod
    def aggregate(self, time: int, energy: float):
        pass  # pragma: no cover

    @abstractmethod
    def calc_superposition_coeffs(self, time: int, time_step: int) -> tuple:
        pass  # pragma: no cover
