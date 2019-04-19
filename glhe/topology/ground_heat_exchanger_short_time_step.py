from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
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

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        # TODO: need to distribute flow properly
        self.inlet_temperature = inputs.temperature
        path_inlet_conditions = SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, inputs.temperature)
        path_responses = []
        for path in self.paths:
            path_responses.append(path.simulate_time_step(path_inlet_conditions))

        return_temp, return_flow = self.mix_paths(path_responses)
        return SimulationResponse(inputs.time, inputs.time_step, return_flow, return_temp)

    def mix_paths(self, responses: list) -> tuple:
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
        return sum_mdot_cp_temp / (sum_mdot * ave_cp), sum_mdot

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
