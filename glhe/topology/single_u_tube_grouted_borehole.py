from math import log, pi

from glhe.functions import get_definition_object, init_temp
from glhe.simulation import SimulationEntryPoint, SimulationResponse
from glhe.properties import PropertiesBase, fluid, soil
from glhe.topology.pipe import Pipe
from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment, TimeStepStructure
from glhe.topology.single_u_tube_pass_through_segment import SingleUTubePassThroughSegment


class Location:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class SingleUTubeGroutedBorehole(SimulationEntryPoint):

    def __init__(self, all_inputs, ghe_inputs):
        SimulationEntryPoint.__init__(self, all_inputs)

        # get borehole definition data
        if 'average-borehole' in ghe_inputs:
            bh_inputs = {'location': {'x': 0, 'y': 0, 'z': 0}}
            bh_def_inputs = {'length': ghe_inputs['average-borehole']['length'],
                             'diameter': ghe_inputs['average-borehole']['diameter'],
                             'shank-spacing': ghe_inputs['average-borehole']['shank-spacing'],
                             'segments': 1}
            grout_inputs = {'name': "Grout",
                            'conductivity': ghe_inputs['average-borehole']['grout-conductivity'],
                            'density': ghe_inputs['average-borehole']['grout-density'],
                            'specific-heat': ghe_inputs['average-borehole']['grout-specific-heat']}
        else:
            bh_name = "bh 1"  # TODO: Get this programmatically
            bh_inputs = get_definition_object(all_inputs, 'borehole', bh_name)
            bh_def_inputs = get_definition_object(all_inputs, 'borehole-definitions', bh_inputs['borehole-def-name'])
            grout_inputs = get_definition_object(all_inputs, 'grout-definitions', bh_def_inputs['grout-def-name'])

        # init geometry
        self.h = bh_def_inputs['length']
        self.diameter = bh_def_inputs['diameter']
        self.radius = self.diameter / 2
        self.shank_space = bh_def_inputs['shank-spacing']

        # bh location
        self.location = Location(bh_inputs['location']['x'], bh_inputs['location']['y'], bh_inputs['location']['z'])
        self.grout = PropertiesBase(grout_inputs)

        # init pipes
        self.num_pipes = 2
        if 'average-borehole' in ghe_inputs:
            pipe_inputs = {'average-pipe': {'inner-diameter': ghe_inputs['average-borehole']['pipe-inner-diameter'],
                                            'outer-diameter': ghe_inputs['average-borehole']['pipe-outer-diameter'],
                                            'conductivity': ghe_inputs['average-borehole']['pipe-conductivity'],
                                            'density': ghe_inputs['average-borehole']['pipe-density'],
                                            'specific-heat': ghe_inputs['average-borehole']['pipe-specific-heat']},
                           'length': ghe_inputs['average-borehole']['length']}
        else:
            pipe_inputs = {'pipe-def-name': bh_def_inputs['pipe-def-name'], 'length': self.h}

        pipe_inputs['length'] = pipe_inputs['length']

        pipe_inputs['name'] = '{}: Pipe 1'.format(ghe_inputs['name'])
        self.pipe_1 = Pipe(all_inputs, pipe_inputs)
        pipe_inputs['name'] = '{}: Pipe 2'.format(ghe_inputs['name'])
        self.pipe_2 = Pipe(all_inputs, pipe_inputs)
        self.pipe_2.apply_transit_delay = False

        if 'number-iterations' in bh_def_inputs:
            self.num_iterations = bh_def_inputs['number-iterations']
        else:
            self.num_iterations = 2

        # init segments
        self.segments = []

        if 'segments' in bh_def_inputs:
            self.num_segments = bh_def_inputs['segments']
        else:
            self.num_segments = 1
        seg_length = self.h / self.num_segments
        if 'average-borehole' in ghe_inputs:
            seg_inputs = {'length': seg_length,
                          'diameter': self.diameter,
                          'segment-name': 'BH:{}:Seg:0'.format(ghe_inputs['name']),
                          'average-grout': grout_inputs,
                          'average-pipe': pipe_inputs['average-pipe']}
        else:
            seg_inputs = {'length': seg_length,
                          'diameter': self.diameter,
                          'segment-name': 'BH:{}:Seg:0'.format(ghe_inputs['name']),
                          'grout-def-name': bh_def_inputs['grout-def-name'],
                          'pipe-def-name': bh_def_inputs['pipe-def-name']}

        if 'grout-fraction' in bh_def_inputs:
            seg_inputs['grout-fraction'] = bh_def_inputs['grout-fraction']
        else:
            seg_inputs['grout-fraction'] = 0.5

        for idx in range(self.num_segments):
            seg_inputs['segment-name'] = 'BH:{}:Seg:{}'.format(ghe_inputs['name'], idx + 1)
            self.segments.append(SingleUTubeGroutedSegment(all_inputs, seg_inputs))

        # final segment is a pass-through segment that connects the U-tube nodes
        seg_inputs['segment-name'] = 'BH:{}:Seg:{}'.format(ghe_inputs['name'], self.num_segments + 1)
        self.segments.append(SingleUTubePassThroughSegment())

        # multi-pole method parameters
        self.resist_bh_ave = None
        self.resist_bh_total_internal = None
        self.resist_bh_grout = None
        self.resist_bh_effective = None
        self.resist_bh_direct_coupling = None
        self.theta_1 = self.shank_space / (2 * self.radius)
        self.theta_2 = self.radius / self.pipe_1.outer_radius
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        sigma_num = self.grout.conductivity - soil.conductivity
        sigma_den = self.grout.conductivity + soil.conductivity
        self.sigma = sigma_num / sigma_den
        self.beta = None

        # report variables
        self.heat_rate = 0
        self.heat_rate_bh = 0
        self.inlet_temperature = init_temp()
        self.outlet_temperature = init_temp()

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
                                                               pipe_resist) - self.pipe_1.resist_pipe / 2.0
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
        pt_2 = (self.h / (fluid.cp(temperature) * flow_rate)) ** 2
        resist_short_circuiting = pt_1 * pt_2

        self.resist_bh_effective = self.resist_bh_ave + resist_short_circuiting
        return self.resist_bh_effective

    def calc_direct_coupling_resistance(self, temperature: float,
                                        flow_rate: float = None,
                                        pipe_resist: float = None) -> tuple:

        r_a = self.calc_bh_total_internal_resistance(temperature, flow_rate, pipe_resist)
        r_b = self.calc_bh_average_resistance(temperature, flow_rate, pipe_resist)

        r_12 = (4 * r_a * r_b) / (4 * r_b - r_a)

        # reset if negative
        if r_12 < 0:
            r_12 = 70

        self.resist_bh_direct_coupling = r_12
        return self.resist_bh_direct_coupling, r_b

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
            raise ValueError("'flow_rate' and 'pipe_resist' cannot both be passed.")  # pragma: no cover
        elif flow_rate:
            self.beta = 2 * pi * self.grout.conductivity * self.pipe_1.calc_resist(flow_rate, temperature)
            return self.beta
        elif pipe_resist:
            # setting pipe resistance directly
            # used for validation
            self.pipe_1.resist_pipe = pipe_resist
            self.beta = 2 * pi * self.grout.conductivity * pipe_resist
            return self.beta
        else:
            raise ValueError('Must pass flow rate or a pipe resistance.')  # pragma: no cover

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:

        time = inputs.time
        time_step = inputs.time_step
        flow_rate = inputs.flow_rate
        inlet_temp = inputs.temperature
        bh_wall_temp = inputs.bh_wall_temp

        r_12, r_b = self.calc_direct_coupling_resistance(inlet_temp, flow_rate=flow_rate)

        seg_inputs = TimeStepStructure(boundary_temp=bh_wall_temp, bh_resist=r_b, flow_rate=flow_rate, dc_resist=r_12)

        self.pipe_1.simulate_time_step(SimulationResponse(time, time_step, flow_rate, inlet_temp))

        for _ in range(self.num_iterations):

            for idx, seg in enumerate(self.segments):

                if idx == 0:
                    seg_inputs.inlet_temp_1 = self.pipe_1.outlet_temperature
                    seg_inputs.inlet_temp_2 = self.segments[idx + 1].get_outlet_2_temp()
                elif idx == self.num_segments:
                    seg_inputs.inlet_temp_1 = self.segments[idx - 1].get_outlet_1_temp()
                else:
                    seg_inputs.inlet_temp_1 = self.segments[idx - 1].get_outlet_1_temp()
                    seg_inputs.inlet_temp_2 = self.segments[idx + 1].get_outlet_2_temp()

                seg.simulate_time_step(time_step, seg_inputs)

        self.pipe_2.simulate_time_step(SimulationResponse(time, time_step, flow_rate, self.get_outlet_temp()))

        # update report variables
        self.inlet_temperature = inlet_temp
        self.outlet_temperature = self.pipe_2.outlet_temperature
        cp = fluid.cp(inlet_temp)
        self.heat_rate = flow_rate * cp * (inlet_temp - self.outlet_temperature)
        self.heat_rate_bh = self.get_heat_rate_bh()

        return SimulationResponse(time, time_step, flow_rate, self.get_outlet_temp())

    def get_outlet_temp(self):
        return self.segments[0].get_outlet_2_temp()

    def get_heat_rate_bh(self):
        bh_ht_rate = 0
        for seg in self.segments:
            if hasattr(seg, 'heat_rate_bh'):
                bh_ht_rate += seg.heat_rate_bh
        return bh_ht_rate
