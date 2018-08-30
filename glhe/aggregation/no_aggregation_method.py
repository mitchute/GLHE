from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.types import AggregationType


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)
        self.type = AggregationType.NOAGG

    def add_load(self, bin_width, sim_time):
        self.loads.appendleft(BaseBin(energy=0, width=bin_width))
        self.update_time()

    def aggregate(self, sim_time):
        pass
