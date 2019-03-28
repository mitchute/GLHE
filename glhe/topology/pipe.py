import numpy as np
from math import log, pi, sqrt

from glhe.globals.functions import smoothing_function
from glhe.globals.functions import tdma_1
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.properties.base_properties import PropertiesBase


class Pipe(PropertiesBase, SimulationEntryPoint):
    Type = ComponentTypes.Pipe

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['name'])

        # input/output processor
        self.ip = ip
        self.op = op

        # load the properties from the definitions
        pipe_props = ip.get_input_object('pipe-definitions', inputs['pipe-def-name'])

        # init the properties
        PropertiesBase.__init__(self, pipe_props)

        # local fluids reference
        self.fluid = self.ip.props_mgr.fluid

        # key geometric parameters
        self.inner_diameter = pipe_props["inner-diameter"]
        self.outer_diameter = pipe_props["outer-diameter"]
        self.length = inputs['length']
        self.init_temp = self.ip.init_temp()

        # compute radii and thickness
        self.wall_thickness = (self.outer_diameter - self.inner_diameter) / 2
        self.inner_radius = self.inner_diameter / 2
        self.outer_radius = self.outer_diameter / 2

        # compute cross-sectional areas
        self.area_cr_inner = pi / 4 * self.inner_diameter ** 2
        self.area_cr_outer = pi / 4 * self.outer_diameter ** 2
        self.area_cr_pipe = self.area_cr_outer - self.area_cr_inner

        # compute surface areas
        self.area_s_inner = pi * self.inner_diameter * self.length
        self.area_s_outer = pi * self.outer_diameter * self.length

        # compute volumes
        self.total_vol = self.area_cr_outer * self.length
        self.fluid_vol = self.area_cr_inner * self.length
        self.pipe_wall_vol = self.area_cr_pipe * self.length

        # other inits
        self.friction_factor = 0
        self.resist_pipe = 0
        self.num_pipe_cells = 64
        self.cell_temps = np.full(self.num_pipe_cells, ip.init_temp())

    def calc_transit_time(self, flow_rate: float, temperature: float) -> float:
        """
        Compute transit time of pipe.

        :param flow_rate: mass flow rate, kg/s
        :param temperature: temperature, C
        :return: transit time, s
        """
        v_dot = flow_rate / self.fluid.get_rho(temperature)
        return self.fluid_vol / v_dot

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        """
        Simulate the temperature response of an adiabatic pipe with internal fluid mixing.

        Rees, S.J. 2015. 'An extended two-dimensional borehole heat exchanger model for
        simulation of short and medium timescale thermal response.' Renewable Energy. 83: 518-526.

        Skoglund, T, and P. Dejmek. 2007. 'A dynamic object-oriented model for efficient
        simulation of fluid dispersion in turbulent flow with varying fluid properties.'
        Chem. Eng. Sci.. 62: 2168-2178.

        Bischoff, K.B., and O. Levenspiel. 1962. 'Fluid dispersion--generalization and comparision
        of mathematical models--II; Comparison of models.' Chem. Eng. Sci.. 17: 257-264.

        :param inputs: inlet conditions
        :return: outlet conditions
        """

        # recommendation by Skoglund
        num_cells = self.num_pipe_cells

        m_dot = inputs.flow_rate
        temp = inputs.temperature
        dt = inputs.time_step

        tau = self.calc_transit_time(m_dot, temp)
        re = self.m_dot_to_re(m_dot, temp)
        r_p = self.inner_radius
        l = self.length

        # Rees Eq. 18
        # Peclet number
        peclet = 1 / (2 * r_p / l * (3.e7 * re ** -2.1 + 1.35 * re ** -0.125))

        # Rees Eq. 17
        # transit time per cell
        tau_n = tau * sqrt(2 / (num_cells * peclet))

        # volume flow rate
        v_dot = m_dot / self.fluid.get_rho(temp)

        # volume per cell
        v_n = tau_n * v_dot

        a = np.full(num_cells - 1, -v_dot)
        b = np.full(num_cells, v_n / dt + v_dot)
        b[0] = 1
        c = np.full(num_cells - 1, 0)
        d = np.full(num_cells, v_n / dt) * self.cell_temps
        d[0] = temp

        self.cell_temps = tdma_1(a, b, c, d)

        return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.flow_rate, self.cell_temps[-1])

    def report_outputs(self) -> dict:
        return {}

    def m_dot_to_re(self, flow_rate, temp):
        """
        Convert mass flow rate to Reynolds number

        :param flow_rate: mass flow rate, kg/s
        :param temp: temperature, C
        :return: Reynolds number
        """
        return 4 * flow_rate / (self.fluid.get_mu(temp) * pi * self.inner_diameter)

    def calc_friction_factor(self, re: float):
        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        low_reynolds = 1500
        high_reynolds = 5000

        if re < low_reynolds:
            self.friction_factor = self.laminar_friction_factor(re)
        elif low_reynolds <= re < high_reynolds:
            f_low = self.laminar_friction_factor(re)

            # pure turbulent flow
            f_high = self.turbulent_friction_factor(re)
            sigma = smoothing_function(re, a=3000, b=450)
            self.friction_factor = (1 - sigma) * f_low + sigma * f_high
        else:
            self.friction_factor = self.turbulent_friction_factor(re)

        return self.friction_factor

    def calc_cond_resist(self):
        """
        Calculates the thermal resistance of a pipe, in [K/(W/m)].

        Javed, S. and Spitler, J.D. 2017. 'Accuracy of borehole thermal resistance calculation methods
        for grouted single U-tube ground heat exchangers.' Applied Energy. 187: 790-806.
        """

        return log(self.outer_diameter / self.inner_diameter) / (2 * pi * self.conductivity)

    def calc_conv_resist(self, flow_rate: float, temp: float):
        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gnielinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.

        :param flow_rate: mass flow rate, kg/s
        :param temp: temperature, C
        :return convection resistance, K/(W/m)
        """

        low_reynolds = 2000
        high_reynolds = 4000

        re = self.m_dot_to_re(flow_rate, temp)

        if re < low_reynolds:
            nu = self.laminar_nusselt()
        elif low_reynolds <= re < high_reynolds:
            nu_low = self.laminar_nusselt()
            nu_high = self.turbulent_nusselt(re, temp)
            sigma = smoothing_function(re, a=3000, b=150)
            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            nu = self.turbulent_nusselt(re, temp)
        return 1 / (nu * pi * self.fluid.get_k(temp))

    def set_resist(self, pipe_resist: float):
        self.resist_pipe = pipe_resist
        return self.resist_pipe

    def calc_resist(self, mass_flow_rate: float, temp: float):
        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. and Spitler, J.D. 2017. 'Accuracy of borehole thermal resistance calculation methods
        for grouted single U-tube ground heat exchangers.' Applied Energy. 187: 790-806.

        Equation 3
        """

        self.resist_pipe = self.calc_conv_resist(mass_flow_rate, temp) + self.calc_cond_resist()
        return self.resist_pipe

    @staticmethod
    def laminar_nusselt():
        """
        Laminar Nusselt number for smooth pipes

        mean(4.36, 3.66)
        :return: Nusselt number
        """
        return 4.01

    def turbulent_nusselt(self, re: float, temp: float):
        """
        Turbulent Nusselt number for smooth pipes

        Gnielinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.

        :param re: Reynolds number
        :param temp: Temperature, C
        :return: Nusselt number
        """

        f = self.calc_friction_factor(re)
        pr = self.fluid.get_pr(temp)
        return (f / 8) * (re - 1000) * pr / (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))

    @staticmethod
    def laminar_friction_factor(re: float):
        """
        Laminar friction factor

        :param re: Reynolds number
        :return: friction factor
        """

        return 64.0 / re

    @staticmethod
    def turbulent_friction_factor(re: float):
        """
        Turbulent friction factor

        :param re: Reynolds number
        :return: friction factor
        """

        return (0.79 * log(re) - 1.64) ** (-2.0)
