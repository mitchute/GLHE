import numpy as np

from glhe.aggregation.agg_types import AggregationTypes
from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.sub_hourly_method import SubHourMethod
from glhe.globals.constants import SEC_IN_HOUR
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor


class DynamicMethod(BaseMethod):
    """
    Dynamic aggregation method.

    Claesson, J. and Javed, S. 2011. 'A load-aggregation method to calculate extraction temperatures
    of borehole heat exchangers.' ASHRAE Winter Conference, Chicago, IL. Jan. 21-25, 2012.
    """

    Type = AggregationTypes.DYNAMIC

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        BaseMethod.__init__(self)
        self.ip = ip
        self.op = op

        self.sub_hr = SubHourMethod()

        # set expansion rate. apply default if needed.
        try:
            self.exp_rate = inputs['expansion-rate']
        except KeyError:
            self.exp_rate = 1.5

        # set the number of bins per level. apply default if needed.
        try:
            self.bins_per_level = inputs['number-bins-per-level']
        except KeyError:
            self.bins_per_level = 9

        # total simulation runtime to make available for method
        run_time = inputs['runtime']

        # time step for method
        # starts at 1 hr steps
        dt = SEC_IN_HOUR

        # method handles from hours 1 to n
        # the first hour (0 to 1) is handled by the sub-hourly method
        # these are referenced from the current simulation time
        t = SEC_IN_HOUR

        # initialize the dynamic method
        initialized = False
        while not initialized:
            for _ in range(self.bins_per_level):
                t += dt
                self.loads = np.insert(self.loads, 0, 0)
                self.dts = np.insert(self.dts, 0, dt)
                self.times = np.insert(self.times, 0, t)
                self.g_vals = np.insert(self.g_vals, 0, 0)

                if t >= run_time:
                    initialized = True

            dt *= self.exp_rate

        # fractions of each bin to be shifted each hour
        self.f = SEC_IN_HOUR / self.dts

        # final bin doesn't shift out any energy, so it's fraction should be 0
        self.f[0] = 0

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
            delta = self.loads * self.f
            self.loads = self.loads - delta
            self.loads = self.loads + np.roll(delta, -1)
            self.loads[-1] += e_1

        # update time
        self.prev_update_time = time
        self.prev_update_time_hr = int(time / SEC_IN_HOUR)
