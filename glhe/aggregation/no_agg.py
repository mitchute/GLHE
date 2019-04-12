import numpy as np

from glhe.aggregation.agg_types import AggregationTypes
from glhe.aggregation.base_agg import BaseAgg


class NoAgg(BaseAgg):
    """
    No aggregation. Just keep all of the values.
    """

    Type = AggregationTypes.NO_AGG

    def __init__(self, inputs):
        BaseAgg.__init__(self, inputs)

    def aggregate(self, time: int, energy: float):
        # check for iteration
        if self.prev_update_time == time:
            return

        # log the values
        self.energy = np.append(self.energy, energy)
        self.times = np.append(self.times, time)

        # update time
        self.prev_update_time = time

    def calc_superposition_coeffs(self, time: int, time_step: int) -> tuple:
        # compute temporal superposition
        # this includes all thermal history before the present time
        tn = time + time_step
        self.dts = np.diff(self.times, append=tn)
        q = self.energy / self.dts
        dq = np.diff(q)

        # g-function values
        lntts = np.log((tn - self.times) / self.ts)
        g = self.interp_g(lntts)

        g_c = g[-1]
        q_prev = q[-1]

        # convolution of delta_q and the g-function values
        hist = float(np.dot(dq, g[:-1]) - q_prev * g_c)
        return float(g_c), hist
