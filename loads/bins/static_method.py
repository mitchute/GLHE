from collections import defaultdict, deque

from loads.bins.static_bin import StaticBin
from loads.bins.base_method import BaseMethod


class StaticMethod(BaseMethod):

    def __init__(self, min_bin_nums, bin_widths):
        BaseMethod.__init__(self)

        self.min_bin_nums = min_bin_nums
        self.bin_widths = bin_widths

    def add_load(self, load):
        self.loads.appendleft(StaticBin(energy=load, width=self.bin_widths[0]))
        self.aggregate()

    def aggregate(self):
        """
        Aggregates the current bins

        :return: none
        """

        # bin the current bin objects into sub-lists to they can be combined as needed
        d = defaultdict(list)
        for i, curr_obj in enumerate(self.loads):
            d[curr_obj.width].append(curr_obj)

        # aggregate within each sub-list, except the last one, which is allowed to grow as needed
        for i, width in enumerate(self.bin_widths[:-1]):
            len_bin = len(d[width])
            if len_bin < int(self.min_bin_nums[i] + self.bin_widths[i + 1] / self.bin_widths[i]):
                # nothing to do here
                pass
            else:
                # merge the bins within this sub-list
                merge_on_obj_index = self.min_bin_nums[i + 1]
                merge_obj_index_start = merge_on_obj_index + 1
                merge_on_obj = d[width][merge_on_obj_index]
                indices_to_pop = []
                for j, obj in enumerate(d[width][merge_obj_index_start:]):
                    merge_on_obj.merge(obj)
                    indices_to_pop.append(j + merge_obj_index_start)

                # throw away unused bins
                for j in reversed(indices_to_pop):
                    d[width].pop(j)

        # redefine the loads
        self.loads = deque()
        for i, bin_width in enumerate(d):
            for j in d[bin_width]:
                self.loads.append(j)
