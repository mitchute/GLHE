from math import pi

from glhe.aggregation.agg_factory import make_agg_method
from glhe.globals.functions import merge_dicts
from glhe.ground_temps.ground_temp_factory import make_ground_temp_model
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes


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

        # load aggregation method
        ts = self.h ** 2 / (9 * self.soil.diffusivity)
        la_inputs = merge_dicts(inputs['load-aggregation'], {'lntts': inputs['lntts'],
                                                             'g-values': inputs['g-values'],
                                                             'lntts_b': inputs['lntts_b'],
                                                             'g_b-values': inputs['g_b-values'],
                                                             'time-scale': ts})
        self.load_agg = make_agg_method(la_inputs, ip)

        # method constant
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

    def simulate_time_step(self, inputs: SimulationResponse):
        time = inputs.time
        dt = inputs.time_step
        flow_rate = inputs.flow_rate
        inlet_temp = inputs.temperature

        # per bh variables
        m_dot_bh = flow_rate / self.num_bh

        # aggregate load from previous time
        # load aggregation method takes care of what happens during iterations
        self.load_agg.aggregate(time, self.energy)

        # solve for outlet temperature
        g_c, hist = self.load_agg.calc_superposition_coeffs(time, dt)
        c_1 = self.c_0 * g_c
        c_2 = self.soil.get_temp(time, self.h) + self.c_0 * hist

        cp = self.fluid.get_cp(inlet_temp)
        m_dot_bh_cp = m_dot_bh * cp

        c_3 = m_dot_bh_cp / self.h
        c_4 = c_3 * inlet_temp

        temp_out = (c_2 + c_1 * c_4) / (1 + c_1 * c_3)

        # total heat transfer rate (W)
        q_tot = flow_rate * cp * (inlet_temp - temp_out)

        # normalized heat transfer rate (W/m)
        self.q = q_tot / (self.h * self.num_bh)

        # energy (J/m)
        self.energy = self.q * dt

        # set report variables
        self.inlet_temperature = inlet_temp
        self.outlet_temperature = temp_out
        self.heat_rate = q_tot

        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temperature)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
