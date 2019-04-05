import numpy as np

from glhe.aggregation.base_method import BaseMethod
from glhe.globals.constants import SEC_IN_HOUR


class SubHourMethod(BaseMethod):
    def __init__(self):
        BaseMethod.__init__(self)
        self.prev_update_time = 0

    def aggregate(self, time, time_step, load):
        self.loads = np.insert(self.loads, 0, load * time_step)
        self.durations = np.insert(self.durations, 0, time_step)
        load_rolled_to_hourly_bin = self.load_rolled_to_hourly_bin()
        return load_rolled_to_hourly_bin

    def load_rolled_to_hourly_bin(self):

        idx_to_shift = []

        sub_hour_times = np.cumsum(self.durations)
        for idx, val in enumerate(np.flip(sub_hour_times)):
            if val >= SEC_IN_HOUR:
                idx_to_shift.append(idx)

        return 0
