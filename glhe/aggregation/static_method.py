from collections import defaultdict, deque

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.static_bin import StaticBin
from glhe.aggregation.types import AggregationType
from glhe.globals.constants import SEC_IN_HOUR


class StaticMethod(BaseMethod):
    Type = AggregationType.STATIC

    def __init__(self, inputs, ip, op):

        self.ip = ip
        self.op = op

        try:
            self.min_num_bins = inputs['minimum-num-bins-for-each-level']
        except KeyError:
            self.min_num_bins = [6, 10, 10, 10, 10]

        try:
            self.bin_durations = inputs['bin-durations-in-hours']
        except KeyError:
            self.bin_durations = [1, 6, 24, 168, 840]

        self.min_sub_hour_bins = int(SEC_IN_HOUR / gv.time_step)

        self.bin_durations = [x * SEC_IN_HOUR for x in self.bin_durations]

        if gv.time_step != SEC_IN_HOUR:
            self.bin_durations.insert(0, gv.time_step)
            self.min_num_bins.insert(0, self.min_sub_hour_bins)

    def get_new_current_load_bin(self, energy=0, width=0):
        self.current_load = StaticBin(energy=energy, width=width)

    def aggregate(self):
        """
        Aggregates the current aggregation

        :return: none
        """

        self.aggregate_current_load()

        # bin the current bin objects into sub-lists to they can be combined as needed
        d = defaultdict(list)
        for i, curr_obj in enumerate(self.loads):
            d[curr_obj.width].append(curr_obj)

        # aggregate within each sub-list, except the last one, which is allowed to grow as needed
        for i, width in enumerate(self.bin_durations[:-1]):
            len_bin = len(d[width])
            if len_bin == 0:
                break
            elif len_bin < int(self.min_num_bins[i] + self.bin_durations[i + 1] / self.bin_durations[i]):
                pass
            else:
                # merge the aggregation within this sub-list
                merge_on_obj_index = self.min_num_bins[i]
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
        for i, bin_width in enumerate(sorted(d)):
            for j in d[bin_width]:
                self.loads.append(j)
