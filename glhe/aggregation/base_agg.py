from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np

from glhe.utilities.functions import InterpolatorBase, Interpolator1D, Interpolator1DFromFile, Interpolator2DFromFile


class BaseAgg(ABC):

    def __init__(self, inputs: dict):
        # g-function values
        if 'g-function-path' in inputs:
            p = Path(inputs['g-function-path'])
            if not p.is_absolute():
                p = Path.cwd() / inputs['g-function-path']
            self.interp_g = Interpolator1DFromFile(p)
        elif 'lntts' and 'g-values' in inputs:
            data_g = np.transpose(np.array([inputs['lntts'], inputs['g-values']]))
            self.interp_g: InterpolatorBase = Interpolator1D(data_g[:, 0], data_g[:, 1])
        else:
            raise KeyError('g-function data not found.')

        # g_b-function values
        self.interp_g_b = None
        if 'g_b-function-path' in inputs:
            p = Path(inputs['g_b-function-path'])
            if not p.is_absolute():
                p = Path.cwd() / inputs['g_b-function-path']
            if 'g_b-flow-rates' in inputs:
                self.interp_g_b: InterpolatorBase = Interpolator2DFromFile(p, inputs['g_b-flow-rates'])
            else:
                self.interp_g_b: InterpolatorBase = Interpolator1DFromFile(p)
        elif 'lntts_b' and 'g_b-values' in inputs:
            data_g_b = np.transpose(np.array([inputs['lntts_b'], inputs['g_b-values']]))
            self.interp_g_b = Interpolator1D(data_g_b[:, 0], data_g_b[:, 1])

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
    def calc_temporal_superposition(self, time_step: int, flow_rate: float = None) -> float:
        pass  # pragma: no cover

    @abstractmethod
    def get_g_value(self, time_step: int) -> float:
        pass  # pragma: no cover

    @abstractmethod
    def get_g_b_value(self, time_step: int, flow_rate: float = None) -> float:
        pass  # pragma: no cover

    @abstractmethod
    def get_q_prev(self) -> float:
        pass  # pragma: no cover
