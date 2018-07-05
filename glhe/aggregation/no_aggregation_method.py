from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)

    def add_load(self, load, width):
        self.loads.appendleft(BaseBin(energy=load, width=width))
