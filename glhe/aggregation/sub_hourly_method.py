import numpy as np

from glhe.aggregation.base_method import BaseMethod


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
        sub_hour_times = np.cumsum(self.durations)

        return 0
