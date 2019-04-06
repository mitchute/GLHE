from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.types import AggregationTypes


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)
        self.type = AggregationTypes.NO_AGG

    def get_new_current_load_bin(self, energy=0, width=0):
        self.current_load = BaseBin(energy=energy, width=width)

    def aggregate(self):
        self.aggregate_current_load()
