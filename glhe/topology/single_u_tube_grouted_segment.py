import numpy as np
from math import pi
from scipy.integrate import solve_ivp

from glhe.input_processor.component_types import ComponentTypes
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase
from glhe.topology.pipe import Pipe


class SingleUTubeGroutedSegment(object):
    Type = ComponentTypes.SegmentSingleUTubeGrouted

    def __init__(self, inputs, ip, op):
        self.name = inputs['segment-name']
        self.ip = ip
        self.op = op

        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        if 'average-pipe' in inputs:

            pipe_inputs = {'average-pipe': inputs['average-pipe'],
                           'length': inputs['length']}
        else:
            pipe_inputs = {'pipe-def-name': inputs['pipe-def-name'], 'length': inputs['length']}

        self.num_pipes = 2
        self.pipe = Pipe(pipe_inputs, ip, op)

        if 'average-grout' in inputs:
            grout_inputs = inputs['average-grout']
        else:
            grout_inputs = ip.get_definition_object('grout-definitions', inputs['grout-def-name'])

        self.grout = PropertiesBase(grout_inputs)

        if 'grout-fraction' in inputs:
            self.grout_frac = inputs['grout-fraction']
        else:
            self.grout_frac = 0.5

        self.length = inputs['length']
        self.diameter = inputs['diameter']
        self.grout_vol = self.calc_grout_volume()

        # four-node model
        self.num_equations = 5

        # computed node temperatures
        self.y = np.full((self.num_equations,), ip.init_temp())

        # time variables
        self.time = 0
        self.time_prev = 0
        self.flow_rate = 0
        self.bh_resist = 0
        self.dc_resist = 0
        self.fluid_cp = 0
        self.fluid_heat_capacity = 0
        self.boundary_temp = ip.init_temp()

        # report variables
        self.inlet_temp_1 = ip.init_temp()
        self.inlet_temp_2 = ip.init_temp()
        self.outlet_temp_1 = ip.init_temp()
        self.outlet_temp_2 = ip.init_temp()
        self.heat_rate_bh = 0

    def calc_grout_volume(self):
        return self.calc_seg_volume() - self.calc_tot_pipe_volume()

    def calc_tot_pipe_volume(self):
        return self.pipe.total_vol * self.num_pipes

    def calc_seg_volume(self):
        return pi / 4 * self.diameter ** 2 * self.length

    def right_hand_side(self, _, y):
        num_equations = self.num_equations
        r = np.zeros(num_equations)

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

    def simulate_time_step(self, time_step: int, inputs: dict) -> np.ndarray:
        self.flow_rate = inputs['flow-rate']
        self.inlet_temp_1 = inputs['inlet-1-temp']
        self.inlet_temp_2 = inputs['inlet-2-temp']
        self.boundary_temp = inputs['boundary-temperature']
        self.bh_resist = inputs['rb']
        self.dc_resist = inputs['dc-resist']
        self.fluid_cp = self.fluid.get_cp(inputs['inlet-1-temp'])
        self.fluid_heat_capacity = self.fluid.get_rho(inputs['inlet-1-temp']) * self.fluid_cp

        ret = solve_ivp(self.right_hand_side, [0, time_step], self.y)
        self.y = ret.y[:, -1]

        # update report vars
        self.heat_rate_bh = self.get_heat_rate_bh()
        self.outlet_temp_1 = self.get_outlet_1_temp()
        self.outlet_temp_2 = self.get_outlet_2_temp()
        return self.y

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp_Leg1): self.inlet_temp_1,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp_Leg1): self.outlet_temp_1,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp_Leg2): self.inlet_temp_2,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp_Leg2): self.outlet_temp_2,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRateBH): self.heat_rate_bh}
