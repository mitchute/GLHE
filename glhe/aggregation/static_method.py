import numpy as np

from glhe.aggregation.agg_types import AggregationTypes
from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.sub_hourly_method import SubHourMethod
from glhe.globals.constants import SEC_IN_HOUR


class StaticMethod(BaseMethod):
    """
    Static aggregation method.

    Yavuzturk, C. and Spitler, J.D. 1999. 'A short time step response factor model for
    vertical ground loop heat exchangers.' ASHRAE Transactions. 105(2):475-485.
    """

    Type = AggregationTypes.STATIC

    def __init__(self, inputs):
        BaseMethod.__init__(self)

        # sub-hourly tracker for the first hour
        self.sub_hr = SubHourMethod()

        # set the minimum bins for each level. apply default if needed.
        try:
            self.min_num_bins = inputs['minimum-num-bins-for-each-level']
        except KeyError:
            self.min_num_bins = [10, 10, 10]

        # set the bin durations for each level. apply default if needed.
        try:
            self.bin_durations = inputs['bin-durations-in-hours']
        except KeyError:
            self.bin_durations = [1, 24, 96, 384]

        # initial values
        self.loads = np.append(self.loads, 0)
        self.dts = np.append(self.dts, self.bin_durations[0] * SEC_IN_HOUR)

        # previous update hour
        self.prev_update_time_hr = 0

    def aggregate(self, time: int, energy: float):
        """
        Aggregate loads. Check for a new time step and aggregate.

        :param time: end sim time of energy value, in seconds. This should be the current sim time.
        :param energy: energy to be logged, in Joules
        """

        # check for iteration
        if self.prev_update_time == time:
            return

        # run through sub-hourly method to track the first hour
        e_1 = self.sub_hr.aggregate(time, energy)

        # only update the long time step aggregation method once per simulation hour
        if int(time / SEC_IN_HOUR) == self.prev_update_time_hr:
            # store whatever rolls off of the sub-hourly method
            self.loads[-1] += e_1
            return
        else:
            # aggregate
            pass

        # update times
        self.prev_update_time = time
        self.prev_update_time_hr = int(time / SEC_IN_HOUR)
