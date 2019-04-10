# from math import pi
#
# from numpy import ones, zeros
#
# from glhe.globals.functions import merge_dicts
# from glhe.globals.functions import runge_kutta_fourth_y
# from glhe.topology.borehole_types import BoreholeTypes
# from glhe.topology.pipe import Pipe
# from glhe.topology.segment_base import SegmentBase
#
#
# class SingleUTubeGroutedSegment(SegmentBase):
#
#     def __init__(self, inputs, ip, op):
#         SegmentBase.__init__(self, ip, op)
#
#         self.type = BoreholeTypes.SINGLE_U_TUBE_GROUTED
#
#         self.fluid = fluid_inst
#         self.grout = grout_inst
#         self.soil = soil_inst
#
#         self.NUM_PIPES = 2
#         self.INIT_TEMP = inputs['initial temp']
#         self.LENGTH = inputs['length']
#         self.DIAMETER = inputs['diameter']
#
#         self.pipe_1 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.LENGTH,
#                                                              'initial temp': inputs['initial temp']}),
#                            fluid_inst=fluid_inst)
#
#         self.pipe_2 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.LENGTH,
#                                                              'initial temp': inputs['initial temp']}),
#                            fluid_inst=fluid_inst)
#
#         self.TOTAL_VOL = self.calc_total_volume()
#         self.FLUID_VOL = self.calc_fluid_volume()
#         self.GROUT_VOL = self.calc_grout_volume()
#         self.PIPE_VOL = self.calc_pipe_volume()
#
#         self.NUM_EQUATIONS = 4
#         self.y = ones(self.NUM_EQUATIONS) * self.INIT_TEMP
#
#         self.borehole_wall_temp = self.INIT_TEMP
#         self.inlet_temp_1 = self.INIT_TEMP
#         self.inlet_temp_2 = self.INIT_TEMP
#
#         self.mass_flow_rate = 0
#         self.bh_resist = 0
#         self.direct_coupling_resist = 0
#
#     def calc_total_volume(self):
#         return pi / 4 * self.DIAMETER ** 2 * self.LENGTH
#
#     def calc_fluid_volume(self):
#         return self.pipe_1.fluid_vol + self.pipe_2.fluid_vol
#
#     def calc_grout_volume(self):
#         return self.calc_total_volume() - self.pipe_1.total_vol - self.pipe_2.total_vol
#
#     def calc_pipe_volume(self):
#         return self.pipe_1.pipe_wall_vol + self.pipe_2.pipe_wall_vol
#
#     def right_hand_side(self, y):
#         num_equations = 4
#         r = zeros(num_equations)
#
#         dz = self.LENGTH
#         t_b = self.borehole_wall_temp
#         t_i_1 = self.inlet_temp_1
#         t_i_2 = self.inlet_temp_2
#
#         r_f = 1 / (self.mass_flow_rate * self.fluid.specific_heat)
#         r_b = self.bh_resist
#         r_12 = self.direct_coupling_resist
#
#         c_f_1 = self.fluid.heat_capacity * self.pipe_1.fluid_vol
#         c_f_2 = self.fluid.heat_capacity * self.pipe_2.fluid_vol
#
#         # spilt between inner and outer grout layer
#         f = 0.1
#         c_g_1 = f * self.grout.specific_heat * self.grout.density * self.GROUT_VOL
#         c_g_1 += self.pipe_1.specific_heat * self.pipe_1.density * self.pipe_1.pipe_wall_vol
#
#         c_g_2 = (1 - f) * self.grout.specific_heat * self.grout.density * self.GROUT_VOL
#         c_g_2 += self.pipe_2.specific_heat * self.pipe_2.density * self.pipe_2.pipe_wall_vol
#
#         r[0] = ((t_i_1 - y[0]) / r_f + (y[2] - y[0]) * dz / (r_12 / 2.0) + (y[3] - y[0]) * dz / r_b) / c_f_1
#         r[1] = ((t_i_2 - y[1]) / r_f + (y[2] - y[1]) * dz / (r_12 / 2.0) + (y[3] - y[1]) * dz / r_b) / c_f_2
#         r[2] = ((y[0] - y[2]) * dz / (r_12 / 2.0) + (y[1] - y[2]) * dz / (r_12 / 2.0)) / c_g_1
#         r[3] = ((y[0] - y[3]) * dz / r_b + (y[1] - y[3]) * dz / r_b + (t_b - y[3]) * dz / (r_b / 2.0)) / c_g_2
#
#         return r
#
#     def simulate(self, timestep, **kwargs):
#         self.borehole_wall_temp = kwargs['borehole wall temp']
#         self.inlet_temp_1 = kwargs['inlet 1 temp']
#         self.inlet_temp_2 = kwargs['inlet 2 temp']
#
#         self.mass_flow_rate = kwargs['mass flow rate']
#         self.bh_resist = kwargs['borehole resistance']
#         self.direct_coupling_resist = kwargs['direct coupling resistance']
#
#         self.y = runge_kutta_fourth_y(self.right_hand_side, timestep, y=self.y)
#         return self.y
#
#     def get_outlet_1_temp(self):
#         return self.y[0]
#
#     def get_outlet_2_temp(self):
#         return self.y[1]
