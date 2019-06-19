import os
from abc import ABC, abstractmethod

import numpy as np
from scipy.interpolate import interp1d

from glhe.utilities.functions import load_interp1d

join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


class BaseAgg(ABC):

    def __init__(self, inputs: dict):
        # g-function values
        if 'g-function-path' in inputs:
            path_g = norm(join(cwd, inputs['g-function-path']))
            self.interp_g = load_interp1d(path_g)
        elif 'lntts' and 'g-values' in inputs:
            data_g = np.transpose(np.array([inputs['lntts'], inputs['g-values']]))
            self.interp_g = interp1d(data_g[:, 0], data_g[:, 1], fill_value='extrapolate')
        else:
            raise KeyError('g-function data not found.')

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

        # time step of each respective bin
        self.dts = np.empty((0,), dtype=int)

        # previous time the aggregation method was updated
        self.prev_update_time = 0

    @abstractmethod
    def aggregate(self, time: int, energy: float):
        pass  # pragma: no cover

    @abstractmethod
    def calc_temporal_superposition(self, time_step: int) -> float:
        pass  # pragma: no cover

    @abstractmethod
    def get_g_value(self, time_step: int) -> float:
        pass  # pragma: no cover

    def get_g_b_value(self, time_step: int) -> float:
        pass  # pragma: no cover

    def get_q_prev(self) -> float:
        pass  # pragma: no cover
