from math import pi

from numpy import log

from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase
from glhe.topology.pipe import Pipe
from glhe.topology.segment import Segment


class Borehole(object):
    _count = 0

    def __init__(self, inputs, fluid_instance):

        # Get inputs from json blob
        self._name = inputs["name"]
        self._depth = inputs["depth"]
        self._diameter = inputs["diameter"]
        self._radius = self._diameter / 2
        self._grout = PropertiesBase(conductivity=inputs["grout"]["conductivity"],
                                     density=inputs["grout"]["density"],
                                     specific_heat=inputs["grout"]["specific heat"])
        self._pipe = Pipe(conductivity=inputs["pipe"]["conductivity"],
                          density=inputs["pipe"]["density"],
                          specific_heat=inputs["pipe"]["specific heat"],
                          inner_diameter=inputs["pipe"]["inner diameter"],
                          outer_diameter=inputs["pipe"]["outer diameter"])

        self.shank_space = inputs["shank-spacing"]

        # Keep reference to fluid instance for usage
        self._fluid = fluid_instance

        # Initialize segments
        self._segments = []
        for segment in range(inputs["segments"]):
            self._segments.append(Segment(segment_type=inputs["type"], fluid_instance=self._fluid))

        # pipe inside cross-sectional area
        self._area_i_cr = pi * self._diameter ** 2.0 / 4.0

        # Initialize other parameters
        self.mass_flow_rate = 0
        self.friction_factor = 0.02

        # Multipole method parameters
        self.resist_bh_ave = None
        self.resist_bh_total_internal = None
        self.resist_bh_grout = None
        self.resist_bh = None

        self.theta_1 = self.shank_space / (2 * self._radius)
        self.theta_2 = self.radius / self._pipe.outer_radius
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        self.sigma = (self._grout.conductivity - self._soil.conductivity) / \
                     (self._grout.conductivity + self._soil.conductivity)
        self.beta = None

        self.calc_bh_resistance()

        # Track bh number
        self._bh_num = Borehole._count
        Borehole._count += 1

    def get_flow_resistance(self):
        numerator = 8.0 * self._pipe.friction_factor * (2 * self._depth)
        denominator = (pow(self._pipe.inner_diameter, 5) * self._fluid.dens * pow(pi, 2))
        return numerator / denominator

    def calc_bh_average_resistance(self):
        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 13
        """

        self.beta = 2 * PI * self._grout.conductivity * self._pipe.resist_pipe

        final_term_1 = log(
            self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))
        num_final_term_2 = self.theta_3 ** 2 * \
                           (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
        den_final_term_2_pt_1 = (1 + self.beta) / (1 - self.beta)
        den_final_term_2_pt_2 = self.theta_3 ** 2 * \
                                (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
        den_final_term_2 = den_final_term_2_pt_1 + den_final_term_2_pt_2
        final_term_2 = num_final_term_2 / den_final_term_2

        self.resist_bh_ave = (1 / (4 * PI * self._grout.conductivity)
                              ) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_ave

    def calc_bh_total_internal_resistance(self):
        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 26
        """

        self.beta = 2 * PI * self._grout.conductivity * self._pipe.resist_pipe

        final_term_1 = log(
            ((1 + self.theta_1 ** 2) ** self.sigma) / (self.theta_3 * (1 - self.theta_1 ** 2) ** self.sigma))
        num_term_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4 + 4 * self.sigma * self.theta_1 ** 2) ** 2
        den_term_2_pt_1 = (1 + self.beta) / (1 - self.beta) * (1 - self.theta_1 ** 4) ** 2
        den_term_2_pt_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4) ** 2
        den_term_2_pt_3 = 8 * self.sigma * self.theta_1 ** 2 * self.theta_3 ** 2 * (1 + self.theta_1 ** 4)
        den_term_2 = den_term_2_pt_1 - den_term_2_pt_2 + den_term_2_pt_3
        final_term_2 = num_term_2 / den_term_2

        self.resist_bh_total_internal = (1 / (PI * self._grout.conductivity)) * (
                self.beta + final_term_1 - final_term_2)

        return self.resist_bh_total_internal

    def calc_bh_grout_resistance(self):
        """
        Calculates grout resistance. Use for validation.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' Applied Energy.187:790-806.

        Equation 3
        """

        self.resist_bh_grout = self.calc_bh_average_resistance() - self._pipe.resist_pipe / 2.0

        return self.resist_bh_grout

    def calc_bh_resistance(self):
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

        # only update if flow rate has changed
        if self._pipe.fluid.flow_rate != self._pipe.fluid.flow_rate_prev:
            self.beta = 2 * PI * self._grout.conductivity * self._pipe.calc_pipe_resistance()
            self.calc_bh_average_resistance()
            self.calc_bh_total_internal_resistance()

        resist_short_circuiting = (1 / (3 * self.resist_bh_total_internal)) * (
                    self.depth / self._pipe.fluid.heat_capacity()) ** 2

        self.resist_bh = self.resist_bh_ave + resist_short_circuiting

        return self.resist_bh

    def set_flow_rate(self, mass_flow_rate):
        self.mass_flow_rate = mass_flow_rate
        velocity = mass_flow_rate / (self._fluid.dens * self._area_i_cr)
        reynolds_no = self._fluid.dens * self._pipe.inner_diameter * velocity / self._fluid.visc
        self.calc_friction_factor = self.calc_friction_factor(reynolds_no)
