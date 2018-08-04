from glhe.aggregation.base_bin import BaseBin
from glhe.aggregation.base_method import BaseMethod


class DynamicMethod(BaseMethod):

    def __init__(self, depth=16, exp_rate=2, width=5, start_width=None, end_width=None):
        BaseMethod.__init__(self)

        if start_width is None and end_width is None:
            # for cases when a constant bin width is specified
            for i in range(depth):
                for _ in range(width):
                    self.loads.append(BaseBin(width=pow(exp_rate, i)))
        else:
            # for cases when the bin width is varies for each depth level
            for i in range(depth):
                width = int((1 - i / depth) * (start_width - end_width) + end_width)
                for _ in range(width):
                    self.loads.append(BaseBin(width=pow(exp_rate, i)))

    def add_load(self, load, width, time):

        for i, cur_bin in reversed(list(enumerate(self.loads))[1:]):
            left_bin = self.loads[i - 1]
            delta = left_bin.energy / left_bin.width
            cur_bin.energy += delta
            left_bin.energy -= delta

        self.loads[0].energy += load
