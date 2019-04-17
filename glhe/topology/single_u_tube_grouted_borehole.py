from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase
from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment
from glhe.topology.single_u_tube_pass_through_segment import SingleUTubePassThroughSegment


class SingleUTubeGroutedBorehole(SimulationEntryPoint):
    Type = ComponentTypes.BoreholeSingleUTubeGrouted

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.ip = ip
        self.op = op

        # get borehole definition data
        bh_inputs = ip.get_definition_object('borehole', inputs['name'])
        bh_def_inputs = ip.get_definition_object('borehole-definitions', bh_inputs['borehole-def-name'])

        self.depth = bh_def_inputs['depth']
        self.diameter = bh_def_inputs['diameter']
        self.radius = self.diameter / 2

        # set up base class
        self.shank_space = bh_def_inputs['shank-spacing']
        self.num_pipes = 2

        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil
        self.grout = PropertiesBase(ip.get_definition_object('grout-definitions', bh_def_inputs['grout-def-name']))

        # init segments
        self.segments = []
        self.num_segments = 10  # hard coded for now
        seg_length = self.depth / self.num_segments
        seg_inputs = merge_dicts(inputs, {'length': seg_length})
        for _ in range(self.num_segments):
            self.segments.append(SingleUTubeGroutedSegment())

        # final segment is a pass-through segment that connects the U-tube nodes
        self.segments.append(SingleUTubePassThroughSegment())

        # report variables
        self.heat_rate = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}

    #     # final segment that ties the two legs of the u-tube together.
    #     # segment has no thickness
    #     self.segments.append(make_segment(inputs=seg_inputs,
    #                                       fluid_inst=fluid_inst,
    #                                       grout_inst=self.grout,
    #                                       soil_inst=soil_inst,
    #                                       final_seg=True))
    #
    #     self.pipe = Pipe(inputs=merge_dicts(inputs['pipe-data'], {'length': inputs['depth'] * self.num_pipes,
    #                                                               'initial temp': inputs['initial temp']}),
    #                      fluid_inst=fluid_inst)
    #
    #     # Initialize other parameters
    #     self.mass_flow_rate = 0
    #     self.mass_flow_rate_prev = 0
    #     self.vol_flow_rate = 0
    #     self.friction_factor = 0.02
    #
    #     # Multipole method parameters
    #     self.resist_bh_ave = None
    #     self.resist_bh_total_internal = None
    #     self.resist_bh_grout = None
    #     self.resist_bh_effective = None
    #     self.theta_1 = self.shank_space / (2 * self.radius)
    #     self.theta_2 = self.radius / self.pipe.outer_radius
    #     self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
    #     sigma_num = self.grout.conductivity - self.soil.conductivity
    #     sigma_den = self.grout.conductivity + self.soil.conductivity
    #     self.sigma = sigma_num / sigma_den
    #     self.beta = None
    #
    #     # Init volumes
    #     self.FLUID_VOL = self.calc_fluid_volume()
    #     self.GROUT_VOL = self.calc_grout_volume()
    #     self.PIPE_VOL = self.calc_pipe_volume()
    #
    # def calc_fluid_volume(self):
    #     vol = 0
    #     for seg in self.segments:
    #         vol += seg.calc_fluid_volume()
    #     return vol
    #
    # def calc_grout_volume(self):
    #     vol = 0
    #     for seg in self.segments:
    #         vol += seg.calc_grout_volume()
    #     return vol
    #
    # def calc_pipe_volume(self):
    #     vol = 0
    #     for seg in self.segments:
    #         vol += seg.calc_pipe_volume()
    #     return vol
    #
    # def get_flow_resistance(self):
    #     numerator = 8.0 * self.pipe.friction_factor * (2 * self.length)
    #     denominator = (pow(self.pipe.inner_diameter, 5) * self.fluid.density * pow(pi, 2))
    #     return numerator / denominator
    #
    # def calc_bh_average_resistance(self):
    #     """
    #     Calculates the average thermal resistance of the borehole using the first-order multipole method.
    #
    #     Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
    #     for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.
    #
    #     Equation 13
    #     """
    #
    #     self.beta = 2 * pi * self.grout.conductivity * self.pipe.resist_pipe
    #
    #     final_term_1 = log(self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))
    #
    #     term_2_num = self.theta_3 ** 2 * (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
    #     term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta)
    #     term_2_den_pt_2 = self.theta_3 ** 2 * (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
    #     term_2_den = term_2_den_pt_1 + term_2_den_pt_2
    #     final_term_2 = term_2_num / term_2_den
    #
    #     self.resist_bh_ave = (1 / (4 * pi * self.grout.conductivity)) * (self.beta + final_term_1 - final_term_2)
    #
    #     return self.resist_bh_ave
    #
    # def calc_bh_total_internal_resistance(self):
    #     """
    #     Calculates the total internal thermal resistance of the borehole using the first-order multipole method.
    #
    #     Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
    #     for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.
    #
    #     Equation 26
    #     """
    #
    #     self.beta = 2 * pi * self.grout.conductivity * self.pipe.resist_pipe
    #
    #     term_1_num = (1 + self.theta_1 ** 2) ** self.sigma
    #     term_1_den = self.theta_3 * (1 - self.theta_1 ** 2) ** self.sigma
    #     final_term_1 = log(term_1_num / term_1_den)
    #
    #     term_2_num = self.theta_3 ** 2 * (1 - self.theta_1 ** 4 + 4 * self.sigma * self.theta_1 ** 2) ** 2
    #     term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta) * (1 - self.theta_1 ** 4) ** 2
    #     term_2_den_pt_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4) ** 2
    #     term_2_den_pt_3 = 8 * self.sigma * self.theta_1 ** 2 * self.theta_3 ** 2 * (1 + self.theta_1 ** 4)
    #     term_2_den = term_2_den_pt_1 - term_2_den_pt_2 + term_2_den_pt_3
    #     final_term_2 = term_2_num / term_2_den
    #
    #     self.resist_bh_total_internal = 1 / (pi * self.grout.conductivity) * (self.beta + final_term_1 - final_term_2)
    #
    #     return self.resist_bh_total_internal
    #
    # def calc_bh_grout_resistance(self):
    #     """
    #     Calculates grout resistance. Use for validation.
    #
    #     Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
    #     for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.
    #
    #     Equation 3
    #     """
    #
    #     self.beta = 2 * pi * self.grout.conductivity * self.pipe.resist_pipe
    #
    #     self.resist_bh_grout = self.calc_bh_average_resistance() - self.pipe.resist_pipe / 2.0
    #     return self.resist_bh_grout
    #
    # def calc_bh_effective_resistance(self):
    #     """
    #     Calculates the effective thermal resistance of the borehole assuming a uniform heat flux.
    #
    #     Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
    #     Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.
    #
    #     Eq: 3-67
    #
    #     Coefficients for equations 13 and 26 from Javed & Spitler 2016 calculated here.
    #
    #     Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
    #     for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.
    #
    #     Equation 14
    #     """
    #
    #     self.beta = 2 * pi * self.grout.conductivity * self.pipe.resist_pipe
    #
    #     self.calc_bh_total_internal_resistance()
    #
    #     pt_1 = 1 / (3 * self.resist_bh_total_internal)
    #     pt_2 = (self.length / (self.fluid.specific_heat * self.mass_flow_rate)) ** 2
    #     resist_short_circuiting = pt_1 * pt_2
    #
    #     self.resist_bh_effective = self.resist_bh_ave + resist_short_circuiting
    #
    #     return self.resist_bh_effective
    #
    # def update_beta(self, pipe_resist):
    #     self.beta = 2 * pi * self.grout.conductivity * pipe_resist
    #     return self.beta
    #
    # def set_flow_rate(self, mass_flow_rate):
    #     self.mass_flow_rate_prev = self.mass_flow_rate
    #     self.mass_flow_rate = mass_flow_rate
    #     self.vol_flow_rate = mass_flow_rate / self.fluid.density
    #     self.update_beta(self.pipe.calc_resist(self.mass_flow_rate))
    #     self.calc_bh_total_internal_resistance()
    #     self.calc_bh_average_resistance()
    #     self.calc_bh_effective_resistance()
    #     self.calc_bh_grout_resistance()
    #
    # def simulate_trcm(self, timestep, temp, flow, inputs):
    #
    #     self.set_flow_rate(flow)
    #
    #     fname = 'segment_temps.csv'
    #     if os.path.exists(fname):
    #         os.remove(fname)
    #         f = open(fname, 'w+')
    #         f.close()
    #
    #     resist_dc_num = 2 * self.resist_bh_total_internal * 2 * self.resist_bh_ave
    #     resist_dc_den = 4 * self.resist_bh_ave - self.resist_bh_total_internal
    #     resist_dc = resist_dc_num / resist_dc_den
    #
    #     kwargs = {'borehole wall temp': inputs['borehole wall temp'],
    #               'borehole resistance': self.resist_bh_ave,
    #               'mass flow rate': flow,
    #               'direct coupling resistance': resist_dc}
    #
    #     elapsed_time = 0
    #     self.write_temps(elapsed_time)
    #
    #     while True:
    #
    #         for idx, seg in enumerate(self.segments):
    #
    #             if idx == 0:
    #                 kwargs['inlet 1 temp'] = temp
    #                 kwargs['inlet 2 temp'] = self.segments[idx + 1].get_outlet_2_temp()
    #             elif idx == self.num_segments:
    #                 kwargs['inlet 1 temp'] = self.segments[idx - 1].get_outlet_1_temp()
    #             else:
    #                 kwargs['inlet 1 temp'] = self.segments[idx - 1].get_outlet_1_temp()
    #                 kwargs['inlet 2 temp'] = self.segments[idx + 1].get_outlet_2_temp()
    #
    #             seg.simulate(1, **kwargs)
    #
    #         elapsed_time += 1
    #         self.write_temps(elapsed_time)
    #
    #         if elapsed_time >= timestep:
    #             break
    #
    # def write_temps(self, time):
    #     with open('segment_temps.csv', 'a') as f:
    #         s_1 = '{}'.format(time)
    #         s_2 = '{}'.format(time)
    #         for seg in self.segments:
    #             s_1 += ',{:0.2f}'.format(seg.get_outlet_1_temp())
    #             s_2 += ',{:0.2f}'.format(seg.get_outlet_2_temp())
    #
    #         s_1 += '\n'
    #         s_2 += '\n'
    #
    #         f.write(s_1)
    #         f.write(s_2)
