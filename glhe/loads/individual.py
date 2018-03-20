from collections import OrderedDict

from glhe.loads.base import LoadAggregationBase


class LoadAggregationIndividual(LoadAggregationBase):

    def __init__(self):
        LoadAggregationBase.__init__(self)
        self._loads = OrderedDict()

    def store_load(self, load, curr_time):
        self._loads[curr_time] = load

    def get_load(self, sim_time):
        ret_val = 0
        for k, v in self._loads.items():
            if k <= sim_time:
                ret_val = v
        return ret_val
