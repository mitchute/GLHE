from math import pi

from glhe.aggregation import Dynamic
from glhe.simulation import SimulationEntryPoint, SimulationResponse
from glhe.functions import merge_dicts, init_temp
from glhe.properties import fluid, soil
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class GroundHeatExchangerLTS(SimulationEntryPoint):

    def __init__(self, all_inputs: dict, ghe_inputs: dict):
        SimulationEntryPoint.__init__(self, ghe_inputs)

        # geometry and other config parameters needed externally
        self.h = ghe_inputs['length']
        self.num_bh = ghe_inputs['number-boreholes']
        self.num_paths = len(ghe_inputs['flow-paths'])

        # load aggregation method
        ts = self.h ** 2 / (9 * soil.diffusivity)
        la_inputs = merge_dicts(ghe_inputs['load-aggregation'], {'g-function-path': ghe_inputs['g-function-path'],
                                                             # TODO: Need this? 'g_b-function-path': ghe_inputs['g_b-function-path'],
                                                             'time-scale': ts})

        if 'g_b-flow-rates' in ghe_inputs:
            la_inputs['g_b-flow-rates'] = ghe_inputs['g_b-flow-rates']
        self.load_agg = Dynamic(la_inputs)

        # average borehole
        d_ave_bh = {'average-borehole': ghe_inputs['average-borehole'],
                    'name': 'average-borehole',
                    'borehole-type': 'single-grouted'}
        self.ave_bh = SingleUTubeGroutedBorehole(all_inputs, d_ave_bh)

        self.cross_ghe_present = False
        self.cross_ghe = []
        # if 'cross-loads' in inputs:  # TODO: Is this going to be supported
        #     self.cross_ghe_present = True
        #     for x_ghe in inputs['cross-loads']:
        #         d_x = {'load-aggregation': merge_dicts(inputs['load-aggregation'],
        #                                                {'g-function-path': x_ghe['g-function-path'],
        #                                                 'time-scale': ts}),
        #                'load-data-path': x_ghe['load-data-path'],
        #                'start-time': x_ghe['start-time'],
        #                'length': x_ghe['length']}
        #         if 'number-of-instances' in x_ghe:
        #             num_duplicates = x_ghe['number-of-instances']
        #         else:
        #             num_duplicates = 1
        #         for idx in range(num_duplicates):
        #             self.cross_ghe.append(CrossGHE(d_x, ip, op))

        # method constants
        k_s = soil.conductivity
        self.c_0 = 1 / (2 * pi * k_s)

        # heat rate (W/m)
        self.q = 0

        # energy (J/m)
        self.energy = 0

        # report variables
        self.heat_rate = 0
        self.inlet_temperature = init_temp()
        self.outlet_temperature = init_temp()
        self.bh_wall_temperature = init_temp()
        self.resist_b = 0
        self.resist_b_eff = 0

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        dt = inputs.time_step
        flow_rate = inputs.flow_rate
        inlet_temp = inputs.temperature

        # per bh variables
        flow_rate_path = flow_rate / self.num_paths

        # aggregate load from previous time
        # load aggregation method takes care of what happens during iterations
        self.load_agg.aggregate(time, self.energy)

        # solve for outlet temperature
        g = self.load_agg.get_g_value(dt)
        g_b = self.load_agg.get_g_b_value(dt, flow_rate_path)

        resist_b = self.ave_bh.calc_bh_average_resistance(temperature=inlet_temp, flow_rate=flow_rate)

        hist_g, hist_g_b = self.load_agg.calc_temporal_superposition(dt, flow_rate_path)
        c_1 = self.c_0 * hist_g + resist_b * hist_g_b

        hist_x_ghe = 0
        if self.cross_ghe_present:
            for x_ghe in self.cross_ghe:
                x_ghe.simulate_time_step(dt, time)
                hist_x_ghe += x_ghe.load_agg.calc_temporal_superposition(dt)

        c_1 += self.c_0 * hist_x_ghe

        c_2 = (self.c_0 * g + resist_b * g_b)

        cp = fluid.cp(inlet_temp)
        c_3 = (flow_rate_path * cp) / self.h

        q_prev = self.load_agg.get_q_prev()

        soil_temp = soil.get_temp(time, self.h)
        outlet_temp = (soil_temp + c_2 * c_3 * inlet_temp - c_2 * q_prev + c_1) / (1 + c_2 * c_3)

        # total heat transfer rate (W)
        q_tot = flow_rate * cp * (inlet_temp - outlet_temp)

        # normalized heat transfer rate (W/m)
        self.q = q_tot / (self.h * self.num_bh)

        # energy (J/m)
        self.energy = self.q * dt

        # set report variables
        self.inlet_temperature = inlet_temp
        self.outlet_temperature = outlet_temp
        self.heat_rate = q_tot
        self.resist_b = resist_b
        self.bh_wall_temperature = soil_temp + self.c_0 * (hist_g + hist_x_ghe)
        self.resist_b_eff = self.ave_bh.calc_bh_effective_resistance_uhf(temperature=inlet_temp, flow_rate=flow_rate)

        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temperature)
