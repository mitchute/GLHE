import numpy as np

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.types import AggregationTypes
from glhe.globals.functions import hr_to_sec
from glhe.globals.functions import sec_to_hr
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.aggregation.sub_hourly_method import SubHourMethod


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

        # initialize the dynamic method bins
        sim_time = sec_to_hr(inputs['runtime'])
        cumulative_time = 0
        num_bins = 0
        duration = 1  # hr
        durations = []
        make_bins = True

        while make_bins:
            for _ in range(self.bins_per_level):
                cumulative_time += duration
                durations.append(duration)
                num_bins += 1

                if cumulative_time >= sim_time:
                    make_bins = False
                    break

            duration *= self.exp_rate

        self.loads = np.append(self.loads, np.zeros(num_bins))
        durations = hr_to_sec(np.array(durations))
        self.g_vals = np.zeros(num_bins)
        self.prev_update_time = 0

    def aggregate(self, time: int, energy: float):
        """
        Aggregate loads. Check for a new time step and aggregate.

        :param time: current simulation time, in seconds
        :param energy: new load to be stored, in Watts
        """

        # check for iteration
        if self.prev_update_time == time:
            return

        dt = time - self.prev_update_time



        # aggregate
        delta = self.loads * dt / self.durations
        self.loads - delta
        delta = np.roll(delta, 1)
        delta[0] = energy * dt
        self.loads + delta

        # update sim time
        self.prev_update_time = time
