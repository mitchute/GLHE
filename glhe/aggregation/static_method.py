from collections import defaultdict, deque

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.static_bin import StaticBin
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.variables import gv


class StaticMethod(BaseMethod):

    def __init__(self, inputs=None):
        BaseMethod.__init__(self)

        if inputs is None:
            self.min_bin_nums = [6, 10, 10, 10, 10]
            self.bin_widths = [1, 6, 24, 168, 840]
            self.min_sub_hour_bins = 4
        else:
            try:
                self.min_bin_nums = inputs['min number bins']
            except KeyError:  # pragma: no cover
                raise KeyError("Key: 'min number bins' not found")  # pragma: no cover

            try:
                self.bin_widths = inputs['bin widths in hours']
            except KeyError:  # pragma: no cover
                raise KeyError("Key: 'bin widths in hours' not found")  # pragma: no cover

            try:
                self.min_sub_hour_bins = inputs['min sub-hour bins']
            except KeyError:  # pragma: no cover
                raise KeyError("Key: 'min sub-hour bins' not found")  # pragma: no cover

        self.bin_widths = [x * SEC_IN_HOUR for x in self.bin_widths]
        self.bin_widths.insert(0, gv.time_step)
        self.min_bin_nums.insert(0, self.min_sub_hour_bins)

    def get_most_recent_bin(self):
        if len(self.loads) == 0:
            return StaticBin(0, gv.time_step)
        else:
            return self.loads[0]

    def add_load(self, load, time):
        this_width = time - self.last_time
        self.loads.appendleft(StaticBin(energy=load, width=this_width))
        self.last_time = time

    def update_aggregation(self, time):
        pass  # pragma: no cover

    def aggregate(self):
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
            if len_bin < int(self.min_bin_nums[i] + self.bin_widths[i + 1] / self.bin_widths[i]):
                # nothing to do here
                pass
            else:
                # merge the aggregation within this sub-list
                merge_on_obj_index = self.min_bin_nums[i]
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
