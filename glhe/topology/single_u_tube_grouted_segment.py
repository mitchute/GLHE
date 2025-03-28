import sys
from dataclasses import dataclass
from math import pi

import numpy as np
from scipy.integrate import RK45

from glhe.functions import get_definition_object, init_temp
from glhe.properties import PropertiesBase, fluid
from glhe.topology.pipe import Pipe


@dataclass
class TimeStepStructure:
    flow_rate: float = 0.0
    inlet_temp_1: float = 0.0
    inlet_temp_2: float = 0.0
    boundary_temp: float = 0.0
    bh_resist: float = 0.0
    dc_resist: float = 0.0


class SingleUTubeGroutedSegment:

    def __init__(self, all_inputs, segment_inputs):
        self.name = segment_inputs['segment-name']

        if 'average-pipe' in segment_inputs:
            segment_inputs = {'average-pipe': segment_inputs['average-pipe'], 'length': segment_inputs['length']}
        else:
            segment_inputs = {'pipe-def-name': segment_inputs['pipe-def-name'], 'length': segment_inputs['length']}

        self.num_pipes = 2
        self.pipe = Pipe(all_inputs, segment_inputs)

        if 'average-grout' in segment_inputs:
            grout_inputs = segment_inputs['average-grout']
        else:
            grout_def_name = "standard grout"  # TODO: Get from inputs
            grout_inputs = get_definition_object(all_inputs, 'grout-definitions', grout_def_name)

        self.grout = PropertiesBase(grout_inputs)

        if 'grout-fraction' in segment_inputs:
            self.grout_frac = segment_inputs['grout-fraction']
        else:
            self.grout_frac = 0.5

        self.length = segment_inputs['length']
        self.diameter = 0.114  # TODO: Get from inputs  segment_inputs['diameter']
        self.grout_vol = self.calc_grout_volume()

        # four-node model
        self.num_equations = 5

        # computed node temperatures
        self.y = np.full((self.num_equations,), init_temp())

        # time variables
        self.time = 0
        self.time_prev = 0
        self.flow_rate = 0
        self.bh_resist = 0
        self.dc_resist = 0
        self.fluid_cp = 0
        self.fluid_heat_capacity = 0
        self.boundary_temp = init_temp()

        # report variables
        self.inlet_temp_1 = init_temp()
        self.inlet_temp_2 = init_temp()
        self.outlet_temp_1 = init_temp()
        self.outlet_temp_2 = init_temp()
        self.heat_rate_bh = 0

    def calc_grout_volume(self):
        return self.calc_seg_volume() - self.calc_tot_pipe_volume()

    def calc_tot_pipe_volume(self):
        return self.pipe.total_vol * self.num_pipes

    def calc_seg_volume(self):
        return pi / 4 * self.diameter ** 2 * self.length

    def right_hand_side(self, _, y):
        r = np.zeros(self.num_equations)

        dz = self.length
        t_b = self.boundary_temp
        t_i_1 = self.inlet_temp_1
        t_i_2 = self.inlet_temp_2

        r_f = 1 / (self.flow_rate * self.fluid_cp)
        r_b = self.bh_resist
        r_12 = self.dc_resist

        c_f_1 = self.fluid_heat_capacity * self.pipe.fluid_vol
        c_f_2 = c_f_1

        # direct-coupling grout node
        f = self.grout_frac
        c_g_1 = f * self.grout.specific_heat * self.grout.density * self.grout_vol
        c_g_1 += self.pipe.specific_heat * self.pipe.density * self.pipe.pipe_wall_vol

        # node between leg-1 and wall
        c_g_2 = (1 - f) * self.grout.specific_heat * self.grout.density * self.grout_vol
        c_g_2 += self.pipe.specific_heat * self.pipe.density * self.pipe.pipe_wall_vol
        c_g_2 /= 2

        # node between leg-2 and wall
        c_g_3 = c_g_2

        # fluid node leg 1
        r[0] = ((t_i_1 - y[0]) / r_f + (y[2] - y[0]) * dz / (r_12 / 2.0) + (y[3] - y[0]) * dz / r_b) / c_f_1

        # fluid node leg 2
        r[1] = ((t_i_2 - y[1]) / r_f + (y[2] - y[1]) * dz / (r_12 / 2.0) + (y[4] - y[1]) * dz / r_b) / c_f_2

        # direct-coupling grout node
        r[2] = ((y[0] - y[2]) * dz / (r_12 / 2.0) + (y[1] - y[2]) * dz / (r_12 / 2.0)) / c_g_1

        # leg-1 node
        r[3] = ((y[0] - y[3]) * dz / r_b + + (t_b - y[3]) * dz / r_b) / c_g_2

        # leg-2 node
        r[4] = ((y[1] - y[4]) * dz / r_b + + (t_b - y[4]) * dz / r_b) / c_g_3

        return r

    def get_heat_rate_bh(self):
        q_tot = (self.y[3] - self.boundary_temp) / self.bh_resist * self.length
        q_tot += (self.y[4] - self.boundary_temp) / self.bh_resist * self.length
        return q_tot

    def get_outlet_1_temp(self):
        return self.y[0]

    def get_outlet_2_temp(self):
        return self.y[1]

    def simulate_time_step(self, time_step: float, inputs: TimeStepStructure) -> np.ndarray:
        """
        Simulate a single time step for this segment.  Solves the equations simultaneously using
        RK45 method.
        Parameters
        :param time_step: float Time step in seconds?
        :param inputs: TimeStepStructure of data to begin this time step.
        """
        self.flow_rate = inputs.flow_rate
        self.inlet_temp_1 = inputs.inlet_temp_1
        self.inlet_temp_2 = inputs.inlet_temp_2
        self.boundary_temp = inputs.boundary_temp
        self.bh_resist = inputs.bh_resist
        self.dc_resist = inputs.dc_resist
        self.fluid_cp = fluid.cp(self.inlet_temp_1)
        self.fluid_heat_capacity = fluid.rho(self.inlet_temp_1) * self.fluid_cp

        solver = RK45(self.right_hand_side, 0, self.y, time_step)
        while solver.status != 'finished':
            # print(solver.t, file=sys.stderr)
            solver.step()
        # solver_2 = runge_kutta_fourth_y(self.right_hand_side, time_step, self.y)
        self.y = solver.y

        # update report vars
        self.heat_rate_bh = self.get_heat_rate_bh()
        self.outlet_temp_1 = self.get_outlet_1_temp()
        self.outlet_temp_2 = self.get_outlet_2_temp()
        return self.y
