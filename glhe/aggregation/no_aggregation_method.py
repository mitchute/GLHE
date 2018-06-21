from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod


class NoAggMethod(BaseMethod):
    """
    Loads are not aggregated by this method. Instead, all loads stored and used as previous history.
    """

    def __init__(self):
        BaseMethod.__init__(self)

    def add_load(self, load):
        self.loads.appendleft(BaseBin(energy=load, width=1))
