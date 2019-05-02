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
        la_inputs = merge_dicts(inputs['load-aggregation'], {'g-function-path': inputs['g-function-path'],
                                                             'time-scale': ts})
        self.load_agg = make_agg_method(la_inputs, ip)

        # ground temperature model
        self.gtm = make_ground_temp_model(ip.input_dict['ground-temperature-model'])
        self.temp_g = self.gtm.get_temp()

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

    # TODO: this will have to exercise the STS model to generate the EWT g-functions
    # def generate_sts_response(self):
    #
    #     # output processor for the STS g-functions
    #     sts_op = OutputProcessor(self.op.output_dir, 'out_sts.csv')
    #
    #     # TODO: figure out how to set flow rate(s)
    #     # TODO: dido, but for the load
    #
    #     # load object
    #     lp_inputs = {'name': 'load-4000', 'load-profile-type': 'constant', 'value': 4000}
    #     sts_load = ConstantLoad(lp_inputs, self.ip, sts_op)
    #
    #     # flow object
    #     lf_inputs = {'name': 'flow-0.3', 'flow-profile-type': 'constant', 'value': 0.3}
    #     sts_flow = ConstantFlow(lf_inputs, self.ip, sts_op)
    #
    #     # TODO: how to set these for arbitrary GHE
    #     # sim time parameters
    #     current_sim_time = 0
    #     time_step = 5
    #     end_sim_time = 14400
    #
    #     # log initial state
    #     d_out = {'Elapsed Time [s]': current_sim_time}
    #     d_out = merge_dicts(d_out, self.report_outputs())
    #     d_out = merge_dicts(d_out, sts_load.report_outputs())
    #     sts_op.collect_output(d_out)
    #
    #     response = SimulationResponse(current_sim_time, time_step, 0, self.ip.init_temp())
    #     while True:
    #         response = sts_load.simulate_time_step(response)
    #         response = sts_flow.simulate_time_step(response)
    #         response = self.simulate_time_step(response)
    #         current_sim_time += time_step
    #         d_out = {'Elapsed Time [s]': current_sim_time}
    #         d_out = merge_dicts(d_out, self.report_outputs())
    #         d_out = merge_dicts(d_out, sts_load.report_outputs())
    #         sts_op.collect_output(d_out)
    #
    #         if current_sim_time >= end_sim_time:
    #             break
    #
    #     sts_op.write_to_file()

    def simulate_time_step(self, inputs: SimulationResponse):
        # inputs from upstream component
        temp_in = inputs.temperature
        m_dot = inputs.flow_rate
        time = inputs.time
        dt = inputs.time_step

        # per bh variables
        m_dot_bh = m_dot / self.num_bh

        # aggregate load from previous time
        # load aggregation method takes care of what happens during iterations
        self.load_agg.aggregate(time, self.energy)

        # solve for outlet temperature
        g_c, hist = self.load_agg.calc_superposition_coeffs(time, dt)
        c_1 = self.c_0 * g_c
        c_2 = self.temp_g + self.c_0 * hist

        cp = self.fluid.get_cp(temp_in)
        m_dot_bh_cp = m_dot_bh * cp

        c_3 = m_dot_bh_cp / self.h
        c_4 = c_3 * temp_in

        temp_out = (c_2 + c_1 * c_4) / (1 + c_1 * c_3)

        # total heat transfer rate (W)
        q_tot = m_dot * cp * (temp_in - temp_out)

        # normalized heat transfer rate (W/m)
        self.q = q_tot / (self.h * self.num_bh)

        # energy (J/m)
        self.energy = self.q * dt

        # set report variables
        self.inlet_temperature = temp_in
        self.outlet_temperature = temp_out
        self.heat_rate = q_tot

        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temperature)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
