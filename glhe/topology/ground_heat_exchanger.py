from glhe.globals.constants import SEC_IN_DAY
from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.constant_load import ConstantLoad
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS


class GroundHeatExchanger(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchanger

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # output processor for the STS g-functions
        self.sts_op = OutputProcessor(op.output_dir, 'out_sts.csv')

        # init TRCM model
        self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)
        lp_inputs = {'name': 'load-4000', 'load-profile-type': 'constant', 'value': 4000}
        self.sts_load = ConstantLoad(lp_inputs, ip, op)

        # init g-function model
        ave_depth = self.sts_ghe.calc_ave_depth()
        num_bh = self.sts_ghe.count_bhs()
        lts_inputs = merge_dicts(inputs, {'depth': ave_depth, 'number-boreholes': num_bh})
        self.lts_ghe = GroundHeatExchangerLTS(lts_inputs, ip, op)

        # report variables
        self.heat_rate = 0
        self.inlet_temperature = self.ip.init_temp()
        self.outlet_temperature = self.ip.init_temp()

    def generate_trcm_response(self):
        current_sim_time = 0
        time_step = 30
        end_sim_time = 14400
        d_out = {'Elapsed Time [s]': current_sim_time}
        d_out = merge_dicts(d_out, self.sts_ghe.report_outputs())
        d_out = merge_dicts(d_out, self.sts_load.report_outputs())
        self.sts_op.collect_output(d_out)
        # TODO: figure out how to set flow rate(s)
        # TODO: dido, but for the load
        response = SimulationResponse(current_sim_time, time_step, 0.3, self.ip.init_temp())
        while True:
            response = self.sts_load.simulate_time_step(response)
            response = self.sts_ghe.simulate_time_step(response)
            current_sim_time += time_step
            d_out = {'Elapsed Time [s]': current_sim_time}
            d_out = merge_dicts(d_out, self.sts_ghe.report_outputs())
            d_out = merge_dicts(d_out, self.sts_load.report_outputs())
            self.sts_op.collect_output(d_out)

            if current_sim_time >= end_sim_time:
                break

        self.sts_op.write_to_file()

    def simulate_time_step(self, inputs: SimulationResponse):
        response = self.lts_ghe.simulate_time_step(inputs)

        # update report variables
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = response.temperature
        m_dot = inputs.flow_rate
        cp = self.ip.props_mgr.fluid.get_cp(inputs.temperature)
        self.heat_rate = m_dot * cp * (self.inlet_temperature - self.outlet_temperature)
        return response

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate}
