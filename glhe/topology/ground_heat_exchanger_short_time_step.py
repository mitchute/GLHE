from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.constant_load import ConstantLoad
from glhe.topology.path import Path


class GroundHeatExchangerSTS(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchangerSTS

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # fluid instance
        self.fluid = ip.props_mgr.fluid

        # init paths
        self.paths = []
        for path in inputs['flow-paths']:
            self.paths.append(Path(path, ip, op))

        # report variables
        self.heat_rate = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()

    def calc_ave_depth(self):
        valid_bh_types = [ComponentTypes.BoreholeSingleUTubeGrouted]
        ave_depth = 0
        count = 0
        for path in self.paths:
            for comp in path.components:
                if comp.Type in valid_bh_types:
                    ave_depth += comp.depth
                    count += 1

        return ave_depth / count

    def count_bhs(self):
        valid_bh_types = [ComponentTypes.BoreholeSingleUTubeGrouted]
        count = 0
        for path in self.paths:
            for comp in path.components:
                if comp.Type in valid_bh_types:
                    count += 1

        return count

    def generate_sts_response(self):

        # output processor for the STS g-functions
        sts_op = OutputProcessor(self.op.output_dir, 'out_sts.csv')

        # TODO: figure out how to set flow rate(s)
        # TODO: dido, but for the load

        # load object
        lp_inputs = {'name': 'load-4000', 'load-profile-type': 'constant', 'value': 4000}
        sts_load = ConstantLoad(lp_inputs, self.ip, sts_op)

        # flow object
        lf_inputs = {'name': 'flow-0.3', 'flow-profile-type': 'constant', 'value': 0.3}
        sts_flow = ConstantFlow(lf_inputs, self.ip, sts_op)

        # TODO: how to set these for arbitrary GHE
        # sim time parameters
        current_sim_time = 0
        time_step = 5
        end_sim_time = 14400

        # log initial state
        d_out = {'Elapsed Time [s]': current_sim_time}
        d_out = merge_dicts(d_out, self.report_outputs())
        d_out = merge_dicts(d_out, sts_load.report_outputs())
        sts_op.collect_output(d_out)

        response = SimulationResponse(current_sim_time, time_step, 0, self.ip.init_temp())
        while True:
            response = sts_load.simulate_time_step(response)
            response = sts_flow.simulate_time_step(response)
            response = self.simulate_time_step(response)
            current_sim_time += time_step
            d_out = {'Elapsed Time [s]': current_sim_time}
            d_out = merge_dicts(d_out, self.report_outputs())
            d_out = merge_dicts(d_out, sts_load.report_outputs())
            sts_op.collect_output(d_out)

            if current_sim_time >= end_sim_time:
                break

        sts_op.write_to_file()

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        inlet_temp = inputs.temperature

        # TODO: need to distribute flow properly
        flow = inputs.flow_rate

        path_inlet_conditions = SimulationResponse(inputs.time, inputs.time_step, flow, inlet_temp)
        path_responses = []
        for path in self.paths:
            path_responses.append(path.simulate_time_step(path_inlet_conditions))

        outlet_temp = self.mix_paths(path_responses)

        # update report variables
        cp = self.fluid.get_cp(inlet_temp)

        # TODO: generalize first-law computations everywhere
        self.heat_rate = flow * cp * (inlet_temp - outlet_temp)
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = outlet_temp
        return SimulationResponse(inputs.time, inputs.time_step, flow, outlet_temp)

    def mix_paths(self, responses: list) -> float:
        sum_mdot_cp_temp = 0
        sum_mdot = 0
        sum_cp = 0
        for r in responses:
            temp = r.temperature
            m_dot = r.flow_rate
            cp = self.fluid.get_cp(temp)
            sum_mdot_cp_temp += m_dot * cp * temp
            sum_mdot += m_dot
            sum_cp += cp

        ave_cp = sum_cp / len(responses)
        return sum_mdot_cp_temp / (sum_mdot * ave_cp)

    def report_outputs(self) -> dict:

        d = {}
        for path in self.paths:
            d = merge_dicts(d, path.report_outputs())

        d_self = {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}

        return merge_dicts(d, d_self)
