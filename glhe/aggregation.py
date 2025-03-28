from pathlib import Path

import numpy as np

from glhe.constants import SEC_IN_HOUR
from glhe.functions import InterpolatorBase, Interpolator1D, Interpolator1DFromFile, Interpolator2DFromFile


class BaseAgg:

    def __init__(self, inputs: dict):
        # g-function values
        if 'g-function-path' in inputs:
            # TODO: Get from inputs p = Path(inputs['g-function-path'])
            p = Path('/home/edwin/Projects/GLHE/validation/MFRTRT_EWT_g_functions/EWT_experimental_g_functions.csv')
            if not p.is_absolute():
                p = Path.cwd() / inputs['g-function-path']
            self.interp_g = Interpolator1DFromFile(p)
        elif 'lntts' and 'g-values' in inputs:
            data_g = np.transpose(np.array([inputs['lntts'], inputs['g-values']]))
            self.interp_g: InterpolatorBase = Interpolator1D(data_g[:, 0], data_g[:, 1])
        else:
            raise KeyError('g-function data not found.')

        # g_b-function values
        self.interp_g_b = None
        inputs['g_b-function-path'] = '/home/edwin/Projects/GLHE/validation/MFRTRT_LTS/g_b.csv'
        if 'g_b-function-path' in inputs:
            p = Path(inputs['g_b-function-path'])
            if not p.is_absolute():
                p = Path.cwd() / inputs['g_b-function-path']
            if 'g_b-flow-rates' in inputs:
                self.interp_g_b: InterpolatorBase = Interpolator2DFromFile(p, inputs['g_b-flow-rates'])
            else:
                self.interp_g_b: InterpolatorBase = Interpolator1DFromFile(p)
        elif 'lntts_b' and 'g_b-values' in inputs:
            data_g_b = np.transpose(np.array([inputs['lntts_b'], inputs['g_b-values']]))
            self.interp_g_b = Interpolator1D(data_g_b[:, 0], data_g_b[:, 1])

        self.ts = inputs['time-scale']

        # energy values to be tracked
        self.energy = np.empty((0,), dtype=float)

        # time step of each respective bin
        self.dts = np.empty((0,), dtype=int)

        # previous time the aggregation method was updated
        self.prev_update_time = 0


class SubHour(BaseAgg):
    """
    Sub-hourly load aggregation method. Handles all sub-hourly energy for the first simulation hour.
    """

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


class Dynamic(BaseAgg):
    """
    Dynamic aggregation method.

    Claesson, J. and Javed, S. 2011. 'A load-aggregation method to calculate extraction temperatures
    of borehole heat exchangers.' ASHRAE Winter Conference, Chicago, IL. Jan. 21-25, 2012.
    """

    def __init__(self, inputs: dict):
        BaseAgg.__init__(self, inputs)

        # sub-hourly tracker for the first hour
        self.sub_hr = SubHour(inputs)

        # set expansion rate. apply default if needed.
        self.exp_rate = 1.62
        if 'expansion-rate' in inputs:
            self.exp_rate = inputs['expansion-rate']

        # set the number of bins per level. apply default if needed.
        self.bins_per_level = 9
        if 'number-bins-per-level' in inputs:
            self.bins_per_level = inputs['number-bins-per-level']

        # total simulation runtime to make available for method
        run_time = 14400  # TODO: Get from inputs inputs['runtime']

        # time step for method
        # starts at 1 hr steps
        dt = SEC_IN_HOUR

        # method handles from hours 1 to n
        # the first hour (0 to 1) is handled by the sub-hourly method
        # these are referenced from the current simulation time
        t = SEC_IN_HOUR

        # initialize the dynamic method
        while True:
            for _ in range(self.bins_per_level):
                t += dt
                self.energy = np.insert(self.energy, 0, 0)
                self.dts = np.insert(self.dts, 0, dt)
                if t >= run_time:
                    return
            dt *= self.exp_rate

    def aggregate(self, time: int, energy: float):
        """
        Aggregate energy. Check for a new time step and aggregate.

        :param time: end sim time of energy value, in seconds. This should be the current sim time.
        :param energy: energy to be logged, in Joules
        """

        # check for iteration.
        # if time is the same as previous, we're iterating. so do nothing.
        # else, aggregate the energy
        if self.prev_update_time == time:
            return

        # run through sub-hourly method to track the first hour
        e_1 = self.sub_hr.aggregate(time, energy)

        # fraction of each bin's energy to shift for this time step
        # nothing is shifted out of final bin
        frac_shift = (time - self.prev_update_time) / self.dts
        frac_shift[0] = 0

        delta = self.energy * frac_shift
        self.energy = self.energy - delta
        self.energy = self.energy + np.roll(delta, -1)
        self.energy[-1] += e_1

        # update time
        self.prev_update_time = time

    def calc_temporal_superposition(self, time_step: int, flow_rate: float = None) -> float | tuple[float, float]:

        # compute temporal superposition
        # this includes all thermal history before the present time
        lts_q = self.energy / self.dts
        sts_q = self.sub_hr.energy / self.sub_hr.dts
        q = np.concatenate((lts_q, sts_q))
        dq = np.diff(q, prepend=0)

        # g-function values
        dts = np.append(np.concatenate((self.dts, self.sub_hr.dts)), time_step)
        times = np.flipud(np.cumsum(np.flipud(dts)))[:-1]
        lntts = np.log(times / self.ts)
        g = self.interp_g.interpolate(lntts)

        # convolution of delta_q and the g-function values
        if self.interp_g_b:
            # convolution for "g" and "g_b" g-functions
            if not flow_rate:
                g_b = self.interp_g_b.interpolate(lntts)
            else:
                # TODO: This is not covered by tests, and may need adjusting the interpolator class to work properly
                g_b = np.flipud(self.interp_g_b.interpolate(lntts, flow_rate))
            return float(np.dot(dq, g)), float(np.dot(dq, g_b))
        else:
            # convolution for "g" g-functions only
            return float(np.dot(dq, g))

    def get_g_value(self, time_step: int) -> float:
        lntts = np.log(time_step / self.ts)
        return self.interp_g.interpolate(lntts)

    def get_g_b_value(self, time_step: int, flow_rate: float = None) -> float:
        lntts = np.log(time_step / self.ts)
        return self.interp_g_b.interpolate(lntts, flow_rate)

    def get_q_prev(self) -> float:
        return float(self.sub_hr.energy[-1] / self.sub_hr.dts[-1])
