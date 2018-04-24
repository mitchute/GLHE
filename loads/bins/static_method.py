from loads.bins.base_bin import BaseBin
from loads.bins.base_method import BaseMethod


class StaticMethod(BaseMethod):

    def __init__(self, bin_nums, bin_widths):
        BaseMethod.__init__(self)

        self.bin_nums = bin_nums
        self.bin_widths = bin_widths

    def add_load(self, load):
        self.loads.append(BaseBin(energy=load, width=self.bin_widths[0]))

    def aggregate(self):
        pass
