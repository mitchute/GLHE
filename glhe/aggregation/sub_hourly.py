import numpy as np

from glhe.aggregation.agg_types import AggregationTypes
from glhe.aggregation.base_agg import BaseAgg
from glhe.globals.constants import SEC_IN_HOUR


class SubHour(BaseAgg):
    """
    Sub-hourly load aggregation method. Handles all sub-hourly energy for the first simulation hour.
    """

    Type = AggregationTypes.SUB_HOUR

    def __init__(self, inputs):
        BaseAgg.__init__(self, inputs)
        self.energy = np.append(self.energy, 0)
        self.dts = np.append(self.dts, SEC_IN_HOUR)
        self.prev_update_time = 0

    def aggregate(self, time: int, energy: float):
        """
        Aggregate sub-hourly energy

        :param time: end sim time of energy value, in seconds. This should be the current sim time.
        :param energy: energy to be logged, in Joules
        """

        # check for iteration.
        # if time is the same as previous, we're iterating. so do nothing.
        # else, aggregate the energy
        if self.prev_update_time == time:
            return 0

        # append current values
        self.energy = np.append(self.energy, energy)

        # respective time steps for each bin
        self.dts = np.append(self.dts, time - self.prev_update_time)

        # upper and lower bin edges referenced from current time
        # also, FFR dt_u = time referenced backwards from current time
        dt_u = np.flipud(np.cumsum(np.flipud(self.dts)))
        dt_l = dt_u - self.dts

        # indices from bins where all or part of the load has to be shifted
        idx_full = np.where((dt_l >= SEC_IN_HOUR))[0]
        idx_part = np.where((dt_u > SEC_IN_HOUR) & (dt_l < SEC_IN_HOUR))[0]

        load_to_shift = 0

        # full bins to shift
        if len(idx_full) > 0:
            load_to_shift = np.sum(self.energy[idx_full])

        # partial bin to shift
        if len(idx_part) > 0:
            idx = idx_part[0]
            u_edge = dt_u[idx]
            l_edge = dt_l[idx]
            f = (u_edge - SEC_IN_HOUR) / (u_edge - l_edge)
            load_to_shift += f * self.energy[idx]

            # update the partial bin
            self.energy[idx] = (1 - f) * self.energy[idx]
            self.dts[idx] = (1 - f) * self.dts[idx]

        # finally, delete the values
        self.energy = np.delete(self.energy, idx_full)
        self.dts = np.delete(self.dts, idx_full)

        # update time
        self.prev_update_time = time

        return load_to_shift

    def calc_superposition_coeffs(self, time: int, time_step: int):
        pass
