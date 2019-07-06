from math import pi

from glhe.aggregation.agg_factory import make_agg_method
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.borehole_factory import make_borehole
from glhe.topology.cross_ghe import CrossGHE
from glhe.utilities.functions import merge_dicts


class GroundHeatExchangerLTS(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchangerLTS

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # props instances
        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        # geometry and other config parameters needed externally
        self.h = inputs['length']
        self.num_bh = inputs['number-boreholes']
        self.num_paths = len(inputs['flow-paths'])

        # load aggregation method
        ts = self.h ** 2 / (9 * self.soil.diffusivity)
        la_inputs = merge_dicts(inputs['load-aggregation'], {'g-function-path': inputs['g-function-path'],
                                                             'g_b-function-path': inputs['g_b-function-path'],
                                                             'time-scale': ts})

        if 'g_b-flow-rates' in inputs:
            la_inputs['g_b-flow-rates'] = inputs['g_b-flow-rates']
        self.load_agg = make_agg_method(la_inputs, ip)

        # average borehole
        d_ave_bh = {'average-borehole': inputs['average-borehole'],
                    'name': 'average-borehole',
                    'borehole-type': 'single-grouted'}
        self.ave_bh = make_borehole(d_ave_bh, ip, op)

        self.cross_ghe_present = False
        self.cross_ghe = []
        if 'cross-loads' in inputs:
            self.cross_ghe_present = True
            for x_ghe in inputs['cross-loads']:
                d_x = {'load-aggregation': merge_dicts(inputs['load-aggregation'],
                                                       {'g-function-path': x_ghe['g-function-path'],
                                                        'time-scale': ts}),
                       'load-data-path': x_ghe['load-data-path'],
                       'start-time': x_ghe['start-time'],
                       'length': x_ghe['length']}
                if 'number-of-instances' in x_ghe:
                    num_duplicates = x_ghe['number-of-instances']
                else:
                    num_duplicates = 1
                for idx in range(num_duplicates):
                    self.cross_ghe.append(CrossGHE(d_x, ip, op))

        # method constants
        k_s = self.soil.conductivity
        self.c_0 = 1 / (2 * pi * k_s)

        # heat rate (W/m)
        self.q = 0

        # energy (J/m)
        self.energy = 0

        # report variables
        self.heat_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()
        self.bh_wall_temperature = ip.init_temp()
        self.resist_b = 0
        self.resist_b_eff = 0

    def simulate_time_step(self, inputs: SimulationResponse):
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

        cp = self.fluid.get_cp(inlet_temp)
        c_3 = (flow_rate_path * cp) / self.h

        q_prev = self.load_agg.get_q_prev()

        soil_temp = self.soil.get_temp(time, self.h)
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

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.BHWallTemp): self.bh_wall_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.BHResist): self.resist_b,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.BHEffResist): self.resist_b_eff}
