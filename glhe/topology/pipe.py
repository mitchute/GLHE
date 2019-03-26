from math import pi

from numpy import log

from glhe.globals.functions import smoothing_function
from glhe.properties.base import PropertiesBase


class Pipe(PropertiesBase):

    def __init__(self, inputs, ip, op):
        PropertiesBase.__init__(self, inputs)

        # input/output processor
        self.ip = ip
        self.op = op

        # fluids instance
        self.fluid = self.ip.props_mgr.fluid

        # key geometric parameters
        self.inner_diameter = inputs["inner diameter"]
        self.outer_diameter = inputs["outer diameter"]
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

    # def calc_outlet_temp_hanby(self, temp, v_dot, time_step):
    #
    #     def my_hanby(time):
    #         return hanby(time, v_dot, self.fluid_vol)
    #
    #     transit_time = self.fluid_vol / v_dot
    #
    #     if self.start_up:
    #         idx = 1
    #         while True:
    #
    #             time = time_step * idx
    #             f = my_hanby(time)
    #             tau = time / transit_time
    #             self.temps.append(TempObject(self.init_temp, time_step, time, f, tau))
    #
    #             idx += 1
    #
    #             if self.temps[-1].tau > 1.3:
    #                 self.start_up = False
    #                 break
    #
    #     self.temps.appendleft(TempObject(temp, time_step, 0, my_hanby(time_step), 0))
    #
    #     pop_idxs = []
    #     sum_temp_f = 0
    #     sum_f = 0
    #
    #     for idx, obj in enumerate(self.temps):
    #         obj.time += time_step
    #         obj.f = my_hanby(obj.time)
    #         tau = obj.time / transit_time
    #         obj.tau = tau
    #         if obj.tau > 1.3 and idx != 0:
    #             pop_idxs.append(idx)
    #         else:
    #             sum_temp_f += obj.temp * obj.f
    #             sum_f += obj.f
    #
    #     for idx in reversed(pop_idxs):
    #         if idx == 0:
    #             pass
    #         else:
    #             del self.temps[idx]
    #
    #     ret_temp = sum_temp_f / sum_f
    #
    #     return ret_temp

    def calc_friction_factor(self, re):
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

    def calc_conduction_resistance(self):
        """
        Calculates the thermal resistance of a pipe, in [K/(W/m)].

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        return log(self.outer_diameter / self.inner_diameter) / (2 * pi * self.conductivity)

    def calc_convection_resistance(self, mass_flow_rate):
        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        low_reynolds = 2000
        high_reynolds = 4000

        re = 4 * mass_flow_rate / (self.fluid.viscosity * pi * self.inner_diameter)

        if re < low_reynolds:
            nu = self.laminar_nusselt()
        elif low_reynolds <= re < high_reynolds:
            nu_low = self.laminar_nusselt()
            nu_high = self.turbulent_nusselt(re)
            sigma = smoothing_function(re, a=3000, b=150)
            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            nu = self.turbulent_nusselt(re)
        return 1 / (nu * pi * self.fluid.conductivity)

    def set_resistance(self, pipe_resistance):
        self.resist_pipe = pipe_resistance
        return self.resist_pipe

    def calc_resistance(self, mass_flow_rate):
        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 3
        """

        self.resist_pipe = self.calc_convection_resistance(mass_flow_rate) + self.calc_conduction_resistance()
        return self.resist_pipe

    @staticmethod
    def laminar_nusselt():
        """
        Laminar Nusselt number for smooth pipes

        mean(4.36, 3.66)
        :return: Nusselt number
        """
        return 4.01

    def turbulent_nusselt(self, re):
        """
        Turbulent Nusselt number for smooth pipes

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.

        :param re: Reynolds number
        :return: Nusselt number
        """

        f = self.calc_friction_factor(re)
        pr = self.fluid.prandtl
        return (f / 8) * (re - 1000) * pr / (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))

    @staticmethod
    def laminar_friction_factor(re):
        """
        Laminar friction factor

        :param re: Reynolds number
        :return: friction factor
        """

        return 64.0 / re

    @staticmethod
    def turbulent_friction_factor(re):
        """

        :param re:
        :return:
        """

        return (0.79 * log(re) - 1.64) ** (-2.0)
