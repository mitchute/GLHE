import numpy as np

from glhe.aggregation.base_method import BaseMethod
from glhe.globals.constants import SEC_IN_HOUR


class SubHourMethod(BaseMethod):
    def __init__(self):
        BaseMethod.__init__(self)

        # init arrays
        self.loads = np.append(self.loads, 0)
        self.times = np.append(self.times, 0)

        self.prev_update_time = 0

    def aggregate(self, time, energy):
        """
        Aggregate sub-hourly loads

        :param time: end sim time of energy value, in seconds. This should be the current sim time.
        :param energy: energy to be logged, in Joules
        """

        # check for iteration.
        # if time is the same, we're iterating, so do nothing.
        # else, aggregate the load
        if time == self.prev_update_time:
            return

        # find energy from the previous hour to be shifted
        t_right_edge = time - self.times
        t_left_edge = time - self.times - np.diff(np.append(self.times, time))

        # indices from bins where all or part of the load has to be shifted
        idx_full = np.where((t_left_edge >= SEC_IN_HOUR))[0]
        idx_part = np.where((t_right_edge > SEC_IN_HOUR) & (t_left_edge < SEC_IN_HOUR))[0]

        # append current values
        self.loads = np.append(self.loads, energy)
        self.times = np.append(self.times, time)

        load_to_shift = 0

        # full bins to shift
        if len(idx_full) > 0:
            load_to_shift = np.sum(self.loads[idx_full])

        if len(idx_part) > 0:
            pass

        # finally, delete the values
        self.loads = np.delete(self.loads, np.append(idx_full, idx_part))
        self.times = np.delete(self.times, np.append(idx_full, idx_part))

        # don't forget to insert the partial values here

        # update time
        self.prev_update_time = time

        return load_to_shift
