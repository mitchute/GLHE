from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)

    def add_load(self, load, time):
        width = time - self.last_time
        self.loads.appendleft(BaseBin(energy=load, width=width, abs_time=time))
        self.last_time = time

    def aggregate(self):
        pass  # pragma: no cover
