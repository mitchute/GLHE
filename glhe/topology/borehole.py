from math import pi

import numpy as np

from glhe.properties.base import PropertiesBase
from glhe.properties.pipe import Pipe
from glhe.topology.segment import Segment


class Borehole(object):

    _count = 0

    def __init__(self, inputs, fluid_instance):

        # Get inputs from json blob
        self._name = inputs["name"]
        self._depth = inputs["depth"]
        self._diameter = inputs["diameter"]
        self._grout = PropertiesBase(conductivity=inputs["grout"]["conductivity"],
                                     density=inputs["grout"]["density"],
                                     specific_heat=inputs["grout"]["specific heat"])
        self._pipe = Pipe(conductivity=inputs["pipe"]["conductivity"],
                          density=inputs["pipe"]["density"],
                          specific_heat=inputs["pipe"]["specific heat"],
                          inner_diameter=inputs["pipe"]["inner diameter"],
                          outer_diameter=inputs["pipe"]["outer diameter"])

        # Keep reference to fluid instance for usage
        self._fluid = fluid_instance

        # Initialize segments
        self._segments = []
        for segment in range(inputs["segments"]):
            self._segments.append(Segment(segment_type=inputs["type"], fluid_instance=self._fluid))

        # pipe inside cross-sectional area
        self._area_i_cr = pi * self._diameter ** 2.0 / 4.0

        # Initialize other parameters
        self._mass_flow_rate = 0
        self._friction_factor = 0.02

        # Track bh number
        self._bh_num = Borehole._count
        Borehole._count += 1

    def get_flow_resistance(self):
        return 8.0 * self._friction_factor * (2 * self._depth) / (pow(self._pipe.inner_diameter, 5) * self._fluid.dens * pow(pi, 2))

    @staticmethod
    def friction_factor(re):
        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        lower_limit = 1500
        upper_limit = 5000

        if re < lower_limit:
            return 64.0 / re  # pure laminar flow
        elif lower_limit <= re < upper_limit:
            f_low = 64.0 / re  # pure laminar flow
            # pure turbulent flow
            f_high = (0.79 * np.log(re) - 1.64) ** (-2.0)
            sf = 1 / (1 + np.exp(-(re - 3000.0) / 450.0))  # smoothing function
            return (1 - sf) * f_low + sf * f_high
        else:
            return (0.79 * np.log(re) - 1.64) ** (-2.0)  # pure turbulent flow

    def set_flow_rate(self, mass_flow_rate):
        self._mass_flow_rate = mass_flow_rate
        velocity = mass_flow_rate / (self._fluid.dens * self._area_i_cr)
        reynolds_no = self._fluid.dens * self._pipe.inner_diameter * velocity / self._fluid.visc
        self._friction_factor = self.friction_factor(reynolds_no)
