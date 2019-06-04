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
        dt = time - self.prev_update_time
        self.dts = np.append(self.dts, dt)

        # update time
        self.prev_update_time = time

    def calc_temporal_superposition(self, time_step: int) -> float:
        # compute temporal superposition
        # this includes all thermal history before the present time
        q = self.energy / self.dts
        dq = np.diff(q, prepend=0)

        # g-function values
        dts = np.append(self.dts, time_step)
        times = np.flipud(np.cumsum(np.flipud(dts)))[:-1]
        lntts = np.log(times / self.ts)
        g = self.interp_g(lntts)

        # convolution of delta_q and the g-function values
        if self.interp_g_b:
            # convolution for "g" and "g_b" g-functions
            g_b = self.interp_g_b(lntts)
            return float(np.dot(dq, np.add(g, g_b)))
        else:
            # convolution for "g" g-functions only
            return float(np.dot(dq, g))

    def get_g_value(self, time_step: int) -> float:
        pass  # pragma: no cover

    def get_g_b_value(self, time_step: int) -> float:
        pass  # pragma: no cover

    def get_q_prev(self) -> float:
        pass  # pragma: no cover
