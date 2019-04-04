import numpy as np

from glhe.aggregation.base_method import BaseMethod
from glhe.aggregation.types import AggregationType
from glhe.globals.functions import hr_to_sec
from glhe.globals.functions import sec_to_hr
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor


class DynamicMethod(BaseMethod):
    Type = AggregationType.DYNAMIC

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        BaseMethod.__init__(self)
        self.ip = ip
        self.op = op

        try:
            self.exp_rate = inputs['expansion-rate']
        except KeyError:
            self.exp_rate = 1.5

        try:
            self.bins_per_level = inputs['number-bins-per-level']
        except KeyError:
            self.bins_per_level = 9

        # initialize the dynamic method bins
        sim_time = sec_to_hr(ip.input_dict['simulation']['runtime'])
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

        self.loads = np.append(self.loads, np.zeros(num_bins, dtype=float))
        durations = hr_to_sec(np.array(durations))
        self.durations = np.append(self.durations, durations)
        self.g_vals = np.zeros(num_bins, dtype=float)
        self.prev_update_time = 0

    def aggregate(self, time: int, time_step: int, load: float):
        """
        Aggregate loads. Check for a new time step and aggregate.

        :param time: current simulation time, in seconds
        :param time_step: time step of current iteration, in seconds
        :param load: new load to be stored, in Watts
        """

        # check for iteration
        if self.prev_update_time == time:
            return

        # aggregate
        delta = self.loads * time_step / self.durations
        self.loads - delta
        delta = np.roll(delta, 1)
        delta[0] = load * time_step
        self.loads + delta

        # update sim time
        self.prev_update_time = time
