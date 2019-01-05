from numpy import log

import os

from glhe.globals.constants import PI
from glhe.globals.functions import merge_dicts
from glhe.properties.base import PropertiesBase
from glhe.topology.borehole_base import BoreholeBase
from glhe.topology.borehole_types import BoreholeType
from glhe.topology.pipe import Pipe
from glhe.topology.segment_factory import make_segment


class SingleUTubeGroutedBorehole(BoreholeBase):

    def __init__(self, inputs, fluid_inst, soil_inst):

        BoreholeBase.__init__(self, inputs)

        self.TYPE = BoreholeType.SINGLE_U_TUBE_GROUTED
        self.SHANK_SPACE = inputs['shank-spacing']
        self.DEPTH = inputs['depth']

        self.NUM_PIPES = 2

        self.fluid = fluid_inst
        self.grout = PropertiesBase(inputs=inputs['grout-data'])
        self.soil = soil_inst

        # Initialize segments
        self.segments = []
        self.NUM_SEGMENTS = inputs['segments']
        seg_length = inputs['depth'] / inputs['segments']
        seg_inputs = merge_dicts(inputs, {'length': seg_length})
        for _ in range(self.NUM_SEGMENTS):
            self.segments.append(make_segment(inputs=seg_inputs,
                                              fluid_inst=fluid_inst,
                                              grout_inst=self.grout,
                                              soil_inst=soil_inst))

        # final segment that ties the two legs of the u-tube together.
        # segment has no thickness
        self.segments.append(make_segment(inputs=seg_inputs,
                                          fluid_inst=fluid_inst,
                                          grout_inst=self.grout,
                                          soil_inst=soil_inst,
                                          final_seg=True))

        self.pipe = Pipe(inputs=merge_dicts(inputs['pipe-data'], {'length': inputs['depth'] * self.NUM_PIPES,
                                                                  'initial temp': inputs['initial temp']}),
                         fluid_inst=fluid_inst)

        # Initialize other parameters
        self.mass_flow_rate = 0
        self.mass_flow_rate_prev = 0
        self.vol_flow_rate = 0
        self.friction_factor = 0.02

        # Multipole method parameters
        self.resist_bh_ave = None
        self.resist_bh_total_internal = None
        self.resist_bh_grout = None
        self.resist_bh_effective = None
        self.theta_1 = self.SHANK_SPACE / (2 * self.RADIUS)
        self.theta_2 = self.RADIUS / self.pipe.OUTER_RADIUS
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        sigma_num = self.grout.conductivity - self.soil.conductivity
        sigma_den = self.grout.conductivity + self.soil.conductivity
        self.sigma = sigma_num / sigma_den
        self.beta = None

        # Init volumes
        self.FLUID_VOL = self.calc_fluid_volume()
        self.GROUT_VOL = self.calc_grout_volume()
        self.PIPE_VOL = self.calc_pipe_volume()

    def calc_fluid_volume(self):
        vol = 0
        for seg in self.segments:
            vol += seg.calc_fluid_volume()
        return vol

    def calc_grout_volume(self):
        vol = 0
        for seg in self.segments:
            vol += seg.calc_grout_volume()
        return vol

    def calc_pipe_volume(self):
        vol = 0
        for seg in self.segments:
            vol += seg.calc_pipe_volume()
        return vol

    def get_flow_resistance(self):
        numerator = 8.0 * self.pipe.friction_factor * (2 * self.DEPTH)
        denominator = (pow(self.pipe.INNER_DIAMETER, 5) * self.fluid.density * pow(PI, 2))
        return numerator / denominator

    def calc_bh_average_resistance(self):
        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 13
        """

        self.beta = 2 * PI * self.grout.conductivity * self.pipe.resist_pipe

        final_term_1 = log(self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))

        term_2_num = self.theta_3 ** 2 * (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
        term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta)
        term_2_den_pt_2 = self.theta_3 ** 2 * (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
        term_2_den = term_2_den_pt_1 + term_2_den_pt_2
        final_term_2 = term_2_num / term_2_den

        self.resist_bh_ave = (1 / (4 * PI * self.grout.conductivity)) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_ave

    def calc_bh_total_internal_resistance(self):
        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 26
        """

        self.beta = 2 * PI * self.grout.conductivity * self.pipe.resist_pipe

        term_1_num = (1 + self.theta_1 ** 2) ** self.sigma
        term_1_den = self.theta_3 * (1 - self.theta_1 ** 2) ** self.sigma
        final_term_1 = log(term_1_num / term_1_den)

        term_2_num = self.theta_3 ** 2 * (1 - self.theta_1 ** 4 + 4 * self.sigma * self.theta_1 ** 2) ** 2
        term_2_den_pt_1 = (1 + self.beta) / (1 - self.beta) * (1 - self.theta_1 ** 4) ** 2
        term_2_den_pt_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4) ** 2
        term_2_den_pt_3 = 8 * self.sigma * self.theta_1 ** 2 * self.theta_3 ** 2 * (1 + self.theta_1 ** 4)
        term_2_den = term_2_den_pt_1 - term_2_den_pt_2 + term_2_den_pt_3
        final_term_2 = term_2_num / term_2_den

        self.resist_bh_total_internal = 1 / (PI * self.grout.conductivity) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_total_internal

    def calc_bh_grout_resistance(self):
        """
        Calculates grout resistance. Use for validation.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 3
        """

        self.beta = 2 * PI * self.grout.conductivity * self.pipe.resist_pipe

        self.resist_bh_grout = self.calc_bh_average_resistance() - self.pipe.resist_pipe / 2.0
        return self.resist_bh_grout

    def calc_bh_effective_resistance(self):
        """
        Calculates the effective thermal resistance of the borehole assuming a uniform heat flux.

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.

        Eq: 3-67

        Coefficients for equations 13 and 26 from Javed & Spitler 2016 calculated here.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 14
        """

        self.beta = 2 * PI * self.grout.conductivity * self.pipe.resist_pipe

        self.calc_bh_total_internal_resistance()

        pt_1 = 1 / (3 * self.resist_bh_total_internal)
        pt_2 = (self.DEPTH / (self.fluid.specific_heat * self.mass_flow_rate)) ** 2
        resist_short_circuiting = pt_1 * pt_2

        self.resist_bh_effective = self.resist_bh_ave + resist_short_circuiting

        return self.resist_bh_effective

    def update_beta(self, pipe_resist):
        self.beta = 2 * PI * self.grout.conductivity * pipe_resist
        return self.beta

    def set_flow_rate(self, mass_flow_rate):
        self.mass_flow_rate_prev = self.mass_flow_rate
        self.mass_flow_rate = mass_flow_rate
        self.vol_flow_rate = mass_flow_rate / self.fluid.density
        self.update_beta(self.pipe.calc_resistance(self.mass_flow_rate))
        self.calc_bh_total_internal_resistance()
        self.calc_bh_average_resistance()
        self.calc_bh_effective_resistance()
        self.calc_bh_grout_resistance()

    def simulate_trcm(self, timestep, temp, flow, inputs):

        if os.path.exists('segment_temps.csv'):
            os.remove('segment_temps.csv')
            open('segment_temps.csv', 'w+')

        kwargs = {'borehole wall temp': inputs['borehole wall temp'],
                  'borehole resistance': 0.16,
                  'mass flow rate': flow,
                  'direct coupling resistance': 2.28}

        elapsed_time = 0
        self.write_temps(elapsed_time)

        while True:

            for idx, seg in enumerate(self.segments):

                if idx == 0:
                    kwargs['inlet 1 temp'] = temp
                    kwargs['inlet 2 temp'] = self.segments[idx + 1].get_outlet_2_temp()
                elif idx == self.NUM_SEGMENTS:
                    kwargs['inlet 1 temp'] = self.segments[idx - 1].get_outlet_1_temp()
                else:
                    kwargs['inlet 1 temp'] = self.segments[idx - 1].get_outlet_1_temp()
                    kwargs['inlet 2 temp'] = self.segments[idx + 1].get_outlet_2_temp()

                seg.simulate(1, **kwargs)

            elapsed_time += 1
            self.write_temps(elapsed_time)

            if elapsed_time >= timestep:
                break

    def write_temps(self, time):
        with open('segment_temps.csv', 'a') as f:
            s_1 = '{}'.format(time)
            s_2 = '{}'.format(time)
            for seg in self.segments:
                s_1 += ',{:0.2f}'.format(seg.get_outlet_1_temp())
                s_2 += ',{:0.2f}'.format(seg.get_outlet_2_temp())

            s_1 += '\n'
            s_2 += '\n'

            f.write(s_1)
            f.write(s_2)
