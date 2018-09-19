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
        self.start_width = 5
        self.end_width = 5
        self.num_sub_hour_bins = 4

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

        if self.start_width is None and self.end_width is not None:
            raise ValueError("key 'start width' or key 'end width' is not valid.")  # pragma: no cover
        elif self.start_width is not None and self.end_width is None:
            raise ValueError("key 'start width' or key 'end width' is not valid.")  # pragma: no cover
        elif self.start_width is not None and self.end_width is not None:
            for i in range(self.depth):
                width = int((1 - i / self.depth) * (self.start_width - self.end_width) + self.end_width)
                for _ in range(width):
                    self.loads.append(DynamicBin(width=self.exp_rate ** i))

        self._convert_bins_hours_to_seconds()
        self._add_sts_bins()

    def _add_sts_bins(self):
        for i in range(self.num_sub_hour_bins):
            self.loads.appendleft(DynamicBin(width=gv.time_step))

    def _convert_bins_hours_to_seconds(self):
        for this_bin in self.loads:
            this_bin.width = int(this_bin.width * SEC_IN_HOUR)

    def add_load(self, bin_width, sim_time):
        self.update_time()

    def aggregate(self, sim_time):
        for i, cur_bin in reversed(list(enumerate(self.loads))[1:]):
            left_bin = self.loads[i - 1]
            delta = left_bin.energy * gv.time_step / left_bin.width
            cur_bin.energy += delta
            left_bin.energy -= delta
