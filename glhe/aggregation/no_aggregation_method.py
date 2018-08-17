from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod
from glhe.globals.variables import gv


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)

    def get_most_recent_bin(self):
        if len(self.loads) == 0:
            return BaseBin(0, gv.time_step)
        else:
            return self.loads[0]

    def add_load(self, load, time):
        width = time - self.last_time
        self.loads.appendleft(BaseBin(energy=load, width=width))
        self.last_time = time

    def update_aggregation(self, time):
        pass  # pragma: no cover

    def aggregate(self):
        pass  # pragma: no cover
