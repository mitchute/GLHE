from math import log, pi

from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase
from glhe.topology.pipe import Pipe
from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment
from glhe.topology.single_u_tube_pass_through_segment import SingleUTubePassThroughSegment


class SingleUTubeGroutedBorehole(SimulationEntryPoint):
    Type = ComponentTypes.BoreholeSingleUTubeGrouted

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        # get borehole definition data
        bh_inputs = ip.get_definition_object('borehole', inputs['name'])
        bh_def_inputs = ip.get_definition_object('borehole-definitions', bh_inputs['borehole-def-name'])

        # init geometry
        self.depth = bh_def_inputs['depth']
        self.diameter = bh_def_inputs['diameter']
        self.radius = self.diameter / 2
        self.shank_space = bh_def_inputs['shank-spacing']

        # init grout
        self.grout = PropertiesBase(ip.get_definition_object('grout-definitions', bh_def_inputs['grout-def-name']))

        # init pipes
        self.num_pipes = 2
        pipe_inputs = {'pipe-def-name': bh_def_inputs['pipe-def-name'], 'length': self.depth}
        self.pipe = Pipe(pipe_inputs, ip, op)

        # init segments
        self.segments = []
        self.num_segments = bh_def_inputs['segments']
        seg_length = self.depth / self.num_segments
        seg_inputs = {'length': seg_length,
                      'diameter': self.diameter,
                      'segment-number': 0,
                      'grout-def-name': bh_def_inputs['grout-def-name'],
                      'pipe-def-name': bh_def_inputs['pipe-def-name']}

        for idx in range(self.num_segments):
            seg_inputs['segment-number'] = idx + 1
            self.segments.append(SingleUTubeGroutedSegment(seg_inputs, ip, op))

        # final segment is a pass-through segment that connects the U-tube nodes
        seg_inputs['segment-number'] = self.num_segments + 1
        self.segments.append(SingleUTubePassThroughSegment(seg_inputs, ip, op))

        # multipole method parameters
        self.resist_bh_ave = None
        self.resist_bh_total_internal = None
        self.resist_bh_grout = None
        self.resist_bh_effective = None
        self.theta_1 = self.shank_space / (2 * self.radius)
        self.theta_2 = self.radius / self.pipe.outer_radius
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        sigma_num = self.grout.conductivity - self.soil.conductivity
        sigma_den = self.grout.conductivity + self.soil.conductivity
        self.sigma = sigma_num / sigma_den
        self.beta = None

        # Initialize other parameters
        self.flow_rate = 0
        self.flow_rate_prev = 0
        self.vol_flow_rate = 0
        self.friction_factor = 0.02
        self.update_beta_temp_prev = 0
        self.wall_temperature = ip.init_temp()

        # report variables
        self.heat_rate = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()

    def calc_bh_average_resistance(self, temperature: float,
                                   flow_rate: float = None,
                                   pipe_resist: float = None) -> float:
        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Resistance between the fluid in the U-tube(s) to the borehole wall (m-K/W)

        Javed, S. & Spitler, J.D. 2017. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 13

        :param temperature: temperature, Celsius
        :param flow_rate: mass flow rate, kg/s
        :param pipe_resist: pipe thermal resistance, m-K/W
        """

        self.update_beta(temperature, flow_rate, pipe_resist)

        final_term_1 = log(self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))

        term_2_num = self.theta_3 ** 2 * (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
        term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta)
        term_2_den_pt_2 = self.theta_3 ** 2 * (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
        term_2_den = term_2_den_pt_1 + term_2_den_pt_2
        final_term_2 = term_2_num / term_2_den

        self.resist_bh_ave = (1 / (4 * pi * self.grout.conductivity)) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_ave

    def calc_bh_total_internal_resistance(self, temperature: float,
                                          flow_rate: float = None,
                                          pipe_resist: float = None) -> float:
        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2017. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 26

        :param temperature: temperature, Celsius
        :param flow_rate: mass flow rate, kg/s
        :param pipe_resist: pipe thermal resistance, m-K/W
        """

        self.update_beta(temperature, flow_rate, pipe_resist)

        term_1_num = (1 + self.theta_1 ** 2) ** self.sigma
        term_1_den = self.theta_3 * (1 - self.theta_1 ** 2) ** self.sigma
        final_term_1 = log(term_1_num / term_1_den)

        term_2_num = self.theta_3 ** 2 * (1 - self.theta_1 ** 4 + 4 * self.sigma * self.theta_1 ** 2) ** 2
        term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta) * (1 - self.theta_1 ** 4) ** 2
        term_2_den_pt_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4) ** 2
        term_2_den_pt_3 = 8 * self.sigma * self.theta_1 ** 2 * self.theta_3 ** 2 * (1 + self.theta_1 ** 4)
        term_2_den = term_2_den_pt_1 - term_2_den_pt_2 + term_2_den_pt_3
        final_term_2 = term_2_num / term_2_den

        self.resist_bh_total_internal = 1 / (pi * self.grout.conductivity) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_total_internal

    def calc_bh_grout_resistance(self, temperature: float,
                                 flow_rate: float = None,
                                 pipe_resist: float = None) -> float:
        """
        Calculates grout resistance. Use for validation.

        Javed, S. & Spitler, J.D. 2017. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Eq: 3

        :param temperature: temperature, Celsius
        :param flow_rate: mass flow rate, kg/s
        :param pipe_resist: pipe thermal resistance, m-K/W
        """

        self.update_beta(temperature, flow_rate, pipe_resist)

        self.resist_bh_grout = self.calc_bh_average_resistance(temperature, flow_rate,
                                                               pipe_resist) - self.pipe.resist_pipe / 2.0
        return self.resist_bh_grout

    def calc_bh_effective_resistance_uhf(self, temperature: float,
                                         flow_rate: float = None,
                                         pipe_resist: float = None) -> float:
        """
        Calculates the effective thermal resistance of the borehole assuming a uniform heat flux.

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.

        Eq: 3-67

        :param temperature: temperature, Celsius
        :param flow_rate: mass flow rate, kg/s
        :param pipe_resist: pipe thermal resistance, m-K/W
        """

        self.update_beta(temperature, flow_rate, pipe_resist)

        self.calc_bh_total_internal_resistance(temperature, flow_rate, pipe_resist)
        self.calc_bh_average_resistance(temperature, flow_rate, pipe_resist)

        pt_1 = 1 / (3 * self.resist_bh_total_internal)
        pt_2 = (self.depth / (self.fluid.get_cp(temperature) * self.flow_rate)) ** 2
        resist_short_circuiting = pt_1 * pt_2

        self.resist_bh_effective = self.resist_bh_ave + resist_short_circuiting
        return self.resist_bh_effective

    def update_beta(self, temperature: float, flow_rate: float = None, pipe_resist: float = None) -> float:
        """
        Updates Beta coefficient.

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.

        Eq: 3-47

        Javed, S. & Spitler, J.D. 2017. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Eq: 14

        :param temperature: temperature, Celsius
        :param flow_rate: mass flow rate, kg/s
        :param pipe_resist: pipe thermal resistance, m-K/W
        """

        if flow_rate and pipe_resist:
            # can't set both flow rate and pipe resistance simultaneously
            raise ValueError("'flow_rate' and 'pipe_resist' cannot both be passed.")
        elif flow_rate:
            # check for same conditions as previous call
            if (flow_rate != self.flow_rate_prev) and (temperature != self.update_beta_temp_prev):
                self.flow_rate_prev = self.flow_rate
                self.flow_rate = flow_rate
                self.update_beta_temp_prev = temperature
                self.beta = 2 * pi * self.grout.conductivity * self.pipe.calc_resist(flow_rate, temperature)
            return self.beta
        elif pipe_resist:
            # setting pipe resistance directly
            # used for validation
            self.pipe.resist_pipe = pipe_resist
            self.beta = 2 * pi * self.grout.conductivity * pipe_resist
            return self.beta
        else:
            raise ValueError('Must pass flow rate or a pipe resistance.')

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:

        time = inputs.time
        time_step = inputs.time_step
        flow_rate = inputs.flow_rate
        temperature = inputs.temperature

        r_12 = self.calc_bh_total_internal_resistance(temperature, flow_rate=flow_rate)
        r_b = self.calc_bh_average_resistance(temperature, flow_rate=flow_rate)

        dc_resist_num = 2 * r_12 * 2 * r_b
        dc_resist_den = 4 * r_b - r_12
        dc_resist = dc_resist_num / dc_resist_den

        seg_inputs = {'wall-temperature': self.wall_temperature,
                      'rb': r_b,
                      'flow-rate': flow_rate,
                      'dc-resist': dc_resist}

        for idx, seg in enumerate(self.segments):

            if idx == 0:
                seg_inputs['inlet-1-temp'] = temperature
                seg_inputs['inlet-2-temp'] = self.segments[idx + 1].get_outlet_2_temp()
            elif idx == self.num_segments:
                seg_inputs['inlet-1-temp'] = self.segments[idx - 1].get_outlet_1_temp()
            else:
                seg_inputs['inlet-1-temp'] = self.segments[idx - 1].get_outlet_1_temp()
                seg_inputs['inlet-2-temp'] = self.segments[idx + 1].get_outlet_2_temp()

            seg.simulate_time_step(time_step, seg_inputs)

        return SimulationResponse(time, time_step, flow_rate, self.segments[0].get_outlet_2_temp())

    def report_outputs(self) -> dict:
        d = {}

        for seg in self.segments:
            d = merge_dicts(d, seg.report_outputs())

        d_self = {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}

        return merge_dicts(d, d_self)
