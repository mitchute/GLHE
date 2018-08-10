from abc import ABC, abstractmethod
from collections import deque, namedtuple

from glhe.aggregation.base_bin import BaseBin


class BaseMethod(ABC):

    def __init__(self):
        self.loads = deque()
        self.last_time = 0

    @abstractmethod
    def add_load(self, load, time):
        pass  # pragma: no cover

    @abstractmethod
    def aggregate(self):
        pass  # pragma: no cover

    def get_most_recent_bin(self):
        if len(self.loads) == 0:
            return BaseBin(0, 0, 0)
        else:
            return self.loads[0]

    def reset_to_prev(self):
        self.last_time -= self.loads[0].width
        self.loads.popleft()

    def calc_delta_q(self, current_time):
        ret_vals = []

        LoadHistory = namedtuple('LoadHistory', ['delta_q', 'delta_t'])

        time_from_current = 0

        for i, bin_i in enumerate(self.loads):
            if bin_i == self.loads[0]:
                time_from_current += self.loads[0].width
            elif bin_i == self.loads[-1]:
                ret_vals.append(LoadHistory(bin_i.get_load(), time_from_current))
            else:
                # this occurred farther from the current sim time
                bin_i_minus_1 = self.loads[i + 1]
                load_i = bin_i.get_load()
                load_i_minus_1 = bin_i_minus_1.get_load()
                time_from_current += bin_i_minus_1.width
                ret_vals.append(LoadHistory(load_i - load_i_minus_1, time_from_current))

        if len(ret_vals) == 0:
            ret_vals.append(LoadHistory(0, current_time))

        return ret_vals
