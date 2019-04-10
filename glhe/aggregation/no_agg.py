import numpy as np

from glhe.aggregation.agg_types import AggregationTypes
from glhe.aggregation.base_agg import BaseAgg


class NoAgg(BaseAgg):
    """
    No aggregation. Just keep all of the values.
    """

    Type = AggregationTypes.NO_AGG

    def __init__(self):
        BaseAgg.__init__(self)

    def aggregate(self, time: int, energy: float):
        # check for iteration
        if self.prev_update_time == time:
            return

        # log the values
        self.energy = np.append(self.energy, energy)
        self.dts = np.append(self.dts, time - self.prev_update_time)

        # update time
        self.prev_update_time = time

