from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.dynamic_bin import DynamicBin
from glhe.aggregation.types import AggregationType
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.constants import SEC_IN_YEAR
from glhe.globals.variables import gv


class DynamicMethod(BaseMethod):

    def __init__(self, inputs=None):
        BaseMethod.__init__(self)

        self.type = AggregationType.DYNAMIC

        self.exp_rate = 2
        self.bins_per_level = 5
        self.runtime = SEC_IN_YEAR

        if inputs is not None:
            try:
                self.exp_rate = inputs['expansion rate']
            except KeyError:  # pragma: no cover
                pass  # pragma: no cover

            try:
                self.bins_per_level = inputs['bins per level']
            except KeyError:  # pragma: no cover
                pass

            try:
                self.runtime = inputs['runtime']
            except KeyError:  # pragma: no cover
                pass

        cumulative_time = 0
        bin_width = gv.time_step
        while True:
            for _ in range(self.bins_per_level):
                self.loads.append(DynamicBin(width=bin_width))
                cumulative_time += bin_width
            if cumulative_time > self.runtime:
                break
            else:
                bin_width = int(bin_width * self.exp_rate)

    def get_new_current_load_bin(self, energy=0, width=0):
        self.current_load = DynamicBin(energy=energy, width=width)

    def aggregate(self):

        for i, cur_bin in reversed(list(enumerate(self.loads))[1:]):
            left_bin = self.loads[i - 1]
            delta = left_bin.energy * gv.time_step / left_bin.width
            cur_bin.energy += delta
            left_bin.energy -= delta

        self.loads[0] = self.current_load
