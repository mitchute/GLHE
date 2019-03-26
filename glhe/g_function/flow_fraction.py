from math import exp, log, sin, sqrt

from glhe.globals.constants import gamma_const, pi


class FlowFraction(object):

    def __init__(self, inputs):

        self.l_bh = inputs['BH Depth']
        self.r_b = inputs['BH Radius']
        self.k_s = inputs['Soil Conductivity']
        self.c_s = inputs['Soil Vol Heat Capacity']
        self.c_f = inputs['Fluid Vol Heat Capacity']
        self.v_f = inputs['Fluid Volume']

        self.f = 0
        self.f_prev = 0
        self.t_i_minus_1 = 0

        self.alpha_s = self.k_s / self.c_s

    def calc_flow_fraction(self, sim_time, vol_flow_rate, bh_int_resist, bh_ave_resist):
        """
        Computes the flow fraction based on the method outlined in:

        Beier, R.A., M.S. Mitchell, J.D. Spitler, S. Javed. 2018. 'Validation of borehole heat
        exchanger models against multi-flow rate thermal response tests.' Geothermics 71, 55-68.

        :return flow fraction
        """

        # Define base variables
        t_i = sim_time

        w = vol_flow_rate

        # Transit time
        t_tr = self.v_f / w

        # Equation 3a
        if t_i - self.t_i_minus_1 <= 0.02 * t_tr:
            return self.f_prev  # pragma: no cover

        # total internal borehole resistance
        resist_a = bh_int_resist

        # borehole resistance
        resist_b = bh_ave_resist
        resist_b1 = resist_b * 2

        # Equation 9
        cd_num = self.v_f * self.c_f
        cd_den = 2 * pi * self.l_bh * self.c_s * self.r_b ** 2
        cd = cd_num / cd_den

        # Equation 10
        resist_db = 2 * pi * self.k_s * resist_b

        psi = cd * exp(2 * resist_db)
        phi = log(psi)

        # Equations 11
        if 0.2 < psi <= 1.2:
            tdsf_over_cd = -8.0554 * phi ** 3 + 3.8111 * phi ** 2 - 3.2585 * phi + 2.8004  # pragma: no cover
        elif 1.2 < phi <= 160:
            tdsf_over_cd = -0.2662 * phi ** 4 + 3.5589 * phi ** 3 - 18.311 * phi ** 2 + 57.93 * phi - 6.1661
        elif 160 < phi <= 2E5:  # pragma: no cover
            tdsf_over_cd = 12.506 * phi + 45.051  # pragma: no cover
        else:
            raise ValueError  # pragma: no cover

        # Equation 12
        t_sf_num = tdsf_over_cd * self.c_f * self.v_f
        t_sf_den = 2 * pi * self.l_bh * self.k_s
        t_sf = t_sf_num / t_sf_den + self.t_i_minus_1

        resist_s1 = self.calc_soil_resist(sim_time, bh_ave_resist, self.k_s, self.alpha_s)

        # Equation A.11
        n_a = self.l_bh / (w * self.c_f * resist_a)

        # Equation A.12, A.13
        n_s1 = self.l_bh / (w * self.c_f * (resist_b1 + resist_s1))

        # Equation A.5
        a_1 = (sqrt(4 * ((n_a + n_s1) ** 2 - n_a ** 2))) / 2

        # Equation A.6
        a_2 = -a_1

        # Equation A.7
        c_1 = (n_s1 + a_2) * exp(a_2) / (((n_s1 + a_2) * exp(a_2)) - ((n_s1 + a_1) * exp(a_1)))

        # Equation A.8
        c_2 = 1 - c_1

        # Equation A.9
        c_3 = c_1 * (n_s1 + n_a + a_1) / n_a

        # Equation A.10
        c_4 = c_2 * (n_s1 + n_a + a_2) / n_a

        # Equation A.15
        c_5 = c_1 * (1 + (n_a + n_s1 + a_1) / n_a) * (exp(a_1) - 1) / a_1

        # Equation A.16
        c_6 = (1 - c_1) * (1 + (n_a + n_s1 + a_2) / n_a) * (exp(a_2) - 1) / a_2

        # Equation 5
        f_sf = (0.5 * (c_5 + c_6) - (c_3 + c_4)) / (1 - (c_3 + c_4))

        f_old = self.f_prev

        # Equations 3b and 3c
        if 0.02 * t_tr <= t_i - self.t_i_minus_1 < t_sf:
            _part_1 = (f_sf - f_old) / 2
            log_num = log((t_i - self.t_i_minus_1) / (0.02 * t_tr))
            log_den = log(t_sf / (0.02 * t_tr))
            _part_2 = 1 + sin(pi * (log_num / log_den - 0.5))
            f = _part_1 * _part_2 + f_old
        else:
            f = f_sf  # pragma: no cover

        self.f_prev = f

        return f

    @staticmethod
    def calc_soil_resist(sim_time, bh_resist, soil_cond, soil_diff):
        part_1 = 2 / (4 * pi * soil_cond)
        part_2_num = 4 * soil_diff * sim_time
        if part_2_num == 0:
            soil_resist = 0  # pragma: no cover
        else:
            part_2_den = gamma_const * bh_resist ** 2
            soil_resist = part_1 * log(part_2_num / part_2_den)
            if soil_resist < 0:
                soil_resist = 0

        return soil_resist
