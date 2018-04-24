from loads.bins.base_bin import BaseBin
from loads.bins.base_method import BaseMethod


class NoAggMethod(BaseMethod):

    def __init__(self):
        BaseMethod.__init__(self)

    def add_load(self, load):
        self.loads.appendleft(BaseBin(energy=load, width=1))
