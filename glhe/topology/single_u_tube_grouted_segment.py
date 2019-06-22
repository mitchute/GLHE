import numpy as np
from math import pi
from scipy.integrate import solve_ivp

from glhe.input_processor.component_types import ComponentTypes
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase
from glhe.topology.pipe import Pipe
from glhe.interface.response import SimulationResponse


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

        self.pipe_leg_1 = Pipe(pipe_inputs, ip, op)
        self.pipe_leg_2 = Pipe(pipe_inputs, ip, op)

        if 'average-grout' in inputs:
            grout_inputs = inputs['average-grout']
        else:
            grout_inputs = ip.get_definition_object('grout-definitions', inputs['grout-def-name'])

        self.grout = PropertiesBase(grout_inputs)

        self.length = inputs['length']
        self.diameter = inputs['diameter']
        self.grout_vol = self.calc_grout_volume()

        # six-node model parameters
        # diameter_soil_1 = self.diameter + 0.2
        # diameter_soil_2 = diameter_soil_1 + 0.2
        # k_s = ip.props_mgr.soil.conductivity
        # cp_s = ip.props_mgr.soil.specific_heat
        # rho_s = ip.props_mgr.soil.density
        # vol_s_1 = pi / 4 * (diameter_soil_1 ** 2 - self.diameter ** 2) * self.length
        # vol_s_2 = pi / 4 * (diameter_soil_2 ** 2 - diameter_soil_1 ** 2) * self.length
        # self.resist_s_1 = log(diameter_soil_1 / self.diameter) / (2 * pi * k_s)
        # self.resist_s_2 = log(diameter_soil_2 / diameter_soil_1) / (2 * pi * k_s)
        # self.c_s_1 = rho_s * cp_s * vol_s_1
        # self.c_s_2 = rho_s * cp_s * vol_s_2

        # four-node model
        self.num_equations = 4

        # six-node model
        # self.num_equations = 6

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
        return self.pipe_leg_1.total_vol + self.pipe_leg_1.total_vol

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

        c_f_1 = self.fluid_heat_capacity * self.pipe_leg_1.fluid_vol
        c_f_2 = c_f_1

        # spilt between inner and outer grout layer
        f = 0.1
        c_g_1 = f * self.grout.specific_heat * self.grout.density * self.grout_vol
        c_g_1 += self.pipe_leg_1.specific_heat * self.pipe_leg_1.density * self.pipe_leg_1.pipe_wall_vol

        c_g_2 = (1 - f) * self.grout.specific_heat * self.grout.density * self.grout_vol
        c_g_2 += self.pipe_leg_1.specific_heat * self.pipe_leg_1.density * self.pipe_leg_1.pipe_wall_vol

        # fluid node leg 1
        r[0] = ((t_i_1 - y[0]) / r_f + (y[2] - y[0]) * dz / (r_12 / 2.0) + (y[3] - y[0]) * dz / r_b) / c_f_1

        # fluid node leg 2
        r[1] = ((t_i_2 - y[1]) / r_f + (y[2] - y[1]) * dz / (r_12 / 2.0) + (y[3] - y[1]) * dz / r_b) / c_f_2

        # inner grout node
        r[2] = ((y[0] - y[2]) * dz / (r_12 / 2.0) + (y[1] - y[2]) * dz / (r_12 / 2.0)) / c_g_1

        # four-node model
        # outer grout node
        r[3] = ((y[0] - y[3]) * dz / r_b + (y[1] - y[3]) * dz / r_b + (t_b - y[3]) * dz / (r_b / 2.0)) / c_g_2

        # six-node model
        # outer grout node
        # r[3] = ((y[0] - y[3]) * dz / r_b + (y[1] - y[3]) * dz / r_b + (y[4] - y[3]) * dz / (r_b / 2.0)) / c_g_2

        # borehole wall node
        # r_s_1 = self.resist_s_1
        # c_s_1 = self.c_s_1
        # r[4] = ((y[3] - y[4]) * dz / (r_b / 2.0) + (y[5] - y[4]) * dz / r_s_1) / c_s_1

        # soil node
        # r_s_2 = self.resist_s_2
        # c_s_2 = self.c_s_2
        # r[5] = ((y[4] - y[5]) * dz / r_s_1 + (t_b - y[5]) * dz / r_s_2) / c_s_2

        return r

    def get_heat_rate_bh(self):
        # four-node model
        return (self.y[3] - self.boundary_temp) / (self.bh_resist / 2) * self.length

        # six-node model
        # return (self.y[3] - self.y[4]) / (self.bh_resist / 2) * self.length

    def get_outlet_1_temp(self):
        return self.y[0]

    def get_outlet_2_temp(self):
        return self.y[1]

    def simulate_time_step(self, time: int, time_step: int, inputs: dict) -> np.ndarray:
        self.flow_rate = inputs['flow-rate']
        self.inlet_temp_1 = self.pipe_leg_1.simulate_time_step(SimulationResponse(time,
                                                                                  time_step,
                                                                                  inputs['flow-rate'],
                                                                                  inputs['inlet-1-temp'])).temperature
        self.inlet_temp_2 = self.pipe_leg_2.simulate_time_step(SimulationResponse(time,
                                                                                  time_step,
                                                                                  inputs['flow-rate'],
                                                                                  inputs['inlet-2-temp'])).temperature
        self.boundary_temp = inputs['boundary-temperature']
        self.bh_resist = inputs['rb']
        self.dc_resist = inputs['dc-resist']
        self.fluid_cp = self.fluid.get_cp(inputs['inlet-1-temp'])
        self.fluid_heat_capacity = self.fluid.get_rho(inputs['inlet-1-temp']) * self.fluid_cp
        # self.y = runge_kutta_fourth_y(self.right_hand_side, time_step, y=self.y)

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
