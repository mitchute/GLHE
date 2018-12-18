from collections import deque

from numpy import log

from glhe.globals.constants import PI
from glhe.globals.functions import hanby, smoothing_function
from glhe.properties.base import PropertiesBase


class TempObject(object):
    def __init__(self, temp=0, timestep=0, time=0, f=0, tau=0):
        self.temp = temp
        self.timestep = timestep
        self.time = time
        self.f = f
        self.tau = tau


class Pipe(PropertiesBase):

    def __init__(self, inputs, fluid):
        PropertiesBase.__init__(self, inputs=inputs)
        self.INNER_DIAMETER = inputs["inner diameter"]
        self.OUTER_DIAMETER = inputs["outer diameter"]
        self.LENGTH = inputs['length']
        self.INIT_TEMP = inputs['initial temp']

        self.THICKNESS = (self.OUTER_DIAMETER - self.INNER_DIAMETER) / 2
        self.INNER_RADIUS = self.INNER_DIAMETER / 2
        self.OUTER_RADIUS = self.OUTER_DIAMETER / 2

        self.AREA_CR_OUTER = PI / 4 * self.OUTER_DIAMETER ** 2
        self.AREA_CR_INNER = PI / 4 * self.INNER_DIAMETER ** 2
        self.FLUID_VOL = self.AREA_CR_INNER * self.LENGTH
        self.TOTAL_VOL = self.AREA_CR_OUTER * self.LENGTH
        self.WALL_VOL = (self.AREA_CR_OUTER - self.AREA_CR_INNER) * self.LENGTH

        self.fluid = fluid

        self.friction_factor = 0.02
        self.resist_pipe = 0

        self.temps = deque()
        self.start_up = True

    def calc_outlet_temp_hanby(self, temp, v_dot, time_step):

        def my_hanby(time):
            return hanby(time, v_dot, self.FLUID_VOL)

        transit_time = self.FLUID_VOL / v_dot

        if self.start_up:
            idx = 1
            while True:

                time = time_step * idx
                f = my_hanby(time)
                tau = time / transit_time
                self.temps.append(TempObject(self.INIT_TEMP, time_step, time, f, tau))

                idx += 1

                if self.temps[-1].tau > 1.3:
                    self.start_up = False
                    break

        self.temps.appendleft(TempObject(temp, time_step, 0, my_hanby(time_step), 0))

        pop_idxs = []
        sum_temp_f = 0
        sum_f = 0

        for idx, obj in enumerate(self.temps):
            obj.time += time_step
            obj.f = my_hanby(obj.time)
            tau = obj.time / transit_time
            obj.tau = tau
            if obj.tau > 1.3 and idx != 0:
                pop_idxs.append(idx)
            else:
                sum_temp_f += obj.temp * obj.f
                sum_f += obj.f

        for idx in reversed(pop_idxs):
            if idx == 0:
                pass
            else:
                del self.temps[idx]

        ret_temp = sum_temp_f / sum_f

        return ret_temp

    def calc_friction_factor(self, re):
        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        LOWER_LIMIT = 1500
        UPPER_LIMIT = 5000

        if re < LOWER_LIMIT:
            self.friction_factor = self.laminar_friction_factor(re)
        elif LOWER_LIMIT <= re < UPPER_LIMIT:
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

        return log(self.OUTER_DIAMETER / self.INNER_DIAMETER) / (2 * PI * self.conductivity)

    def calc_convection_resistance(self, mass_flow_rate):
        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        LOWER_LIMIT = 2000
        UPPER_LIMIT = 4000

        re = 4 * mass_flow_rate / (self.fluid.viscosity * PI * self.INNER_DIAMETER)

        if re < LOWER_LIMIT:
            nu = self.laminar_nusselt()
        elif LOWER_LIMIT <= re < UPPER_LIMIT:
            nu_low = self.laminar_nusselt()
            nu_high = self.turbulent_nusselt(re)
            sigma = smoothing_function(re, a=3000, b=150)
            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            nu = self.turbulent_nusselt(re)
        return 1 / (nu * PI * self.fluid.conductivity)

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
