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
        self.dts = np.append(self.dts, time - self.prev_update_time)

        # update time
        self.prev_update_time = time

    def calc_superposition_coeffs(self, time: int, time_step: int) -> tuple:
        # compute temporal superposition
        # this includes all thermal history before the present time
        q = self.energy / self.dts
        dq = np.diff(q, prepend=0)

        # g-function values
        times = np.flipud(np.cumsum(np.flipud(self.dts)))
        lntts = np.log(times / self.ts)
        g = self.interp_g(lntts)

        g_c = self.interp_g(np.log(time_step / self.ts))
        q_prev = q[-1]

        # convolution of delta_q and the g-function values
        hist = float(np.dot(dq, g) - q_prev * g_c)
        return float(g_c), hist

