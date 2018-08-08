from collections import defaultdict, deque

from numpy import array

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.static_bin import StaticBin


class StaticMethod(BaseMethod):

    def __init__(self, inputs=None):
        BaseMethod.__init__(self)

        if inputs is None:
            self.min_bin_nums = [1, 24, 10, 20, 40]
            self.bin_widths = [0, 24, 96, 384, 1536]
        else:
            try:
                self.min_bin_nums = inputs['min number bins']
            except KeyError:
                raise KeyError("Key: 'min number bins' not found")
            try:
                self.bin_widths = inputs['bin widths in hours']
            except KeyError:
                raise KeyError("Key: 'bin widths in hours' not found")

        self.bin_widths = array(self.bin_widths) * 3600

        self.add_load(0, 0)

    def add_load(self, load, time):
        this_width = time - self.last_time
        self.loads.appendleft(StaticBin(energy=load, width=this_width, abs_time=time))
        self._aggregate()
        self.last_time = time

    def _aggregate(self):
        """
        Aggregates the current aggregation

        :return: none
        """

        # bin the current bin objects into sub-lists to they can be combined as needed
        d = defaultdict(list)
        for i, curr_obj in enumerate(self.loads):
            d[curr_obj.width].append(curr_obj)

        # aggregate within each sub-list, except the last one, which is allowed to grow as needed
        for i, width in enumerate(self.bin_widths[:-1]):
            len_bin = len(d[width])
            if self.bin_widths[i] == 0:
                pass
            elif len_bin < int(self.min_bin_nums[i] + self.bin_widths[i + 1] / self.bin_widths[i]):
                # nothing to do here
                pass
            else:
                # merge the aggregation within this sub-list
                merge_on_obj_index = self.min_bin_nums[i + 1]
                merge_obj_index_start = merge_on_obj_index + 1
                merge_on_obj = d[width][merge_on_obj_index]
                indices_to_pop = []
                for j, obj in enumerate(d[width][merge_obj_index_start:]):
                    merge_on_obj.merge(obj)
                    indices_to_pop.append(j + merge_obj_index_start)

                # throw away unused aggregation
                for j in reversed(indices_to_pop):
                    d[width].pop(j)

        # redefine the loads
        self.loads = deque()
        for i, bin_width in enumerate(d):
            for j in d[bin_width]:
                self.loads.append(j)
