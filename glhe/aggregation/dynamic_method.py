from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.variables import gv


class DynamicMethod(BaseMethod):

    def __init__(self, inputs=None):
        BaseMethod.__init__(self)

        self.depth = 16
        self.exp_rate = 2
        self.width = 5
        self.start_width = None
        self.end_width = None
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
                    self.loads.append(BaseBin(width=pow(self.exp_rate, i)))
        else:
            # for cases when the bin width is varies for each depth level
            for i in range(self.depth):
                width = int((1 - i / self.depth) * (self.start_width - self.end_width) + self.end_width)
                for _ in range(width):
                    self.loads.append(BaseBin(width=pow(self.exp_rate, i)))

        self._convert_bins_hours_to_seconds()
        self._add_sts_bins()

    def _add_sts_bins(self):

        # add an extra bin here to give some slack for iterations
        for i in range(self.num_sub_hour_bins + 1):
            self.loads.appendleft(BaseBin(width=gv.time_step))

    def _convert_bins_hours_to_seconds(self):
        for bin in self.loads:
            bin.width *= SEC_IN_HOUR

    def get_most_recent_bin(self):
        return self.loads[1]

    def add_load(self, load, time):
        self.loads[0].energy = load

    def aggregate(self):
        for i, cur_bin in reversed(list(enumerate(self.loads))[self.num_sub_hour_bins + 1:]):
            left_bin = self.loads[i - 1]
            delta = left_bin.energy * gv.time_step / left_bin.width
            cur_bin.energy += delta
            left_bin.energy -= delta

        for i in reversed(range(self.num_sub_hour_bins)):
            self.loads[i + 1].energy = self.loads[i].energy

        self.loads[0].energy = 0

    def reset_to_prev(self):
        self.loads[0].energy = 0
