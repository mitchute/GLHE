from collections import namedtuple

from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)
        self.last_time = 0.0
        self.add_load(0, 0)

    def add_load(self, load, time):
        width = time - self.last_time
        self.loads.appendleft(BaseBin(energy=load, width=width, abs_time=time))
        self.last_time = time

    def reset_to_prev(self):
        self.last_time -= self.loads[0].width
        self.loads.popleft()

    def calc_delta_q(self, current_time):
        ret_vals = []

        LoadHistory = namedtuple('LoadHistory', ['delta_q', 'delta_t'])

        if len(self.loads) < 2:
            bin = self.loads[0]
            ret_vals.append(LoadHistory(bin.get_load(), current_time))
            return ret_vals

        for i in range(len(self.loads) - 1):
            bin_i = self.loads[i]

            # this occurred farther from the current sim time
            bin_i_minus_1 = self.loads[i + 1]

            load_i = bin_i.get_load()
            load_i_minus_1 = bin_i_minus_1.get_load()

            ret_vals.append(LoadHistory(load_i - load_i_minus_1, current_time - bin_i_minus_1.abs_time))

        return ret_vals