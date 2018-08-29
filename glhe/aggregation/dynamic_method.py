from collections import deque

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.dynamic_bin import DynamicBin
from glhe.aggregation.types import AggregationType
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.variables import gv


class DynamicMethod(BaseMethod):

    def __init__(self, inputs=None):
        BaseMethod.__init__(self)

        self.type = AggregationType.DYNAMIC

        self.depth = 16
        self.exp_rate = 2
        self.width = 5
        self.start_width = None
        self.end_width = None
        self.num_sub_hour_bins = 4

        # self.bins = deque()
        self.available_time = 0

        if inputs is not None:
            try:
                self.depth = inputs['depth']
            except KeyError:  # pragma: no cover
                pass  # pragma: no cover

            try:
                self.exp_rate = inputs['expansion rate']
            except KeyError:  # pragma: no cover
                pass  # pragma: no cover

            try:
                self.width = inputs['width']
            except KeyError:  # pragma: no cover
                pass

            try:
                self.start_width = inputs['start width']
            except KeyError:  # pragma: no cover
                pass

            try:
                self.end_width = inputs['end width']
            except KeyError:  # pragma: no cover
                pass

            try:
                self.num_sub_hour_bins = inputs['number of sub-hour bins']
            except KeyError:  # pragma: no cover
                pass

        if (self.start_width is None and self.end_width is not None) or (
                self.start_width is not None and self.end_width is None):
            raise ValueError("key 'start width' or key 'end width' is not valid.")  # pragma: no cover
        elif self.start_width is None and self.end_width is None:
            # for cases when a constant bin width is specified
            for i in range(self.depth):
                for _ in range(self.width):
                    self.loads.append(DynamicBin(width=pow(self.exp_rate, i)))
        else:
            # for cases when the bin width is varies for each depth level
            for i in range(self.depth):
                width = int((1 - i / self.depth) * (self.start_width - self.end_width) + self.end_width)
                for _ in range(width):
                    self.loads.append(DynamicBin(width=pow(self.exp_rate, i)))

        self._convert_bins_hours_to_seconds()
        self._add_sts_bins()

    def _add_sts_bins(self):
        for i in range(self.num_sub_hour_bins):
            self.loads.appendleft(DynamicBin(width=gv.time_step))

    def _convert_bins_hours_to_seconds(self):
        for bin in self.loads:
            bin.width *= SEC_IN_HOUR

    # def _append_bin(self):
    #     new_bin = self.bins[0]
    #     self.loads.append(new_bin)
    #     self.bins.popleft()

    def add_load(self, bin_width, sim_time):
        self.update_time()
        # try:
        #     if sim_time <= self.loads[-1].time and self.loads:
        #         return
        # except IndexError:
        #     pass
        #
        # self._append_bin()

    def aggregate(self, sim_time):

        # if len(self.loads) < self.num_sub_hour_bins:
        #     self._append_bin()
        #     for i in reversed(range(1, len(self.loads))):
        #         delta = self.loads[i - 1].energy
        #         self.loads[i - 1].energy -= delta
        #         self.loads[i].energy += delta
        #     return

        # self.add_load(gv.time_step, sim_time + gv.time_step)

        for i, cur_bin in reversed(list(enumerate(self.loads))[1:]):
            left_bin = self.loads[i - 1]
            delta = left_bin.energy * gv.time_step / left_bin.width
            cur_bin.energy += delta
            left_bin.energy -= delta

        # for i in reversed(range(self.num_sub_hour_bins)):
        #     self.loads[i].energy = self.loads[i - 1].energy

