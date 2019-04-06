import numpy as np

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.types import AggregationTypes
from glhe.globals.constants import SEC_IN_HOUR


class SubHourMethod(BaseMethod):
    Type = AggregationTypes.SUB_HOUR
    """
    Sub-hourly load aggregation method. Handles all sub-hourly loads for the first simulation hour.
    """

    def __init__(self):
        BaseMethod.__init__(self)
        self.prev_update_time = 0

    def aggregate(self, time: int, energy: float):
        """
        Aggregate sub-hourly loads

        :param time: end sim time of energy value, in seconds. This should be the current sim time.
        :param energy: energy to be logged, in Joules
        """

        # check for iteration.
        # if time is the same, we're iterating, so do nothing.
        # else, aggregate the load
        if time == self.prev_update_time:
            return 0

        # append current values
        self.loads = np.append(self.loads, energy)
        self.times = np.append(self.times, time)

        # note that these time steps are not recording the current time steps.
        # they are logging the elapsed time between updates which may be different depending on the current time step.
        self.dts = np.append(self.dts, time - self.prev_update_time)

        # upper and lower bin edges in absolute time
        u_edges = np.flipud(self.times)
        l_edges = u_edges - self.dts

        # upper and lower bin edges referenced from current time
        dt_u = time - self.times + self.dts
        dt_l = time - self.times

        # indices from bins where all or part of the load has to be shifted
        idx_full = np.where((dt_l >= SEC_IN_HOUR))[0]
        idx_part = np.where((dt_u > SEC_IN_HOUR) & (dt_l < SEC_IN_HOUR))[0]

        load_to_shift = 0

        # full bins to shift
        if len(idx_full) > 0:
            load_to_shift = np.sum(self.loads[idx_full])

        # partial bin to shift
        if len(idx_part) > 0:
            idx = idx_part[0]
            u_edge = dt_u[idx]
            l_edge = dt_l[idx]
            f = (u_edge - SEC_IN_HOUR) / (u_edge - l_edge)
            load_to_shift += f * self.loads[idx]
            self.loads[idx] = (1 - f) * self.loads[idx]
            self.times[idx] = (1 - f) * (u_edge - l_edge) + l_edge
            self.dts[idx] = ((1 - f) * (u_edge - l_edge) + l_edge) * self.dts[idx]

        # finally, delete the values
        self.loads = np.delete(self.loads, idx_full)
        self.times = np.delete(self.times, idx_full)
        self.dts = np.delete(self.dts, idx_full)

        # update time
        self.prev_update_time = time

        return load_to_shift
