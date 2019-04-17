from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase


class ExternalFlow(ExternalBase, SimulationEntryPoint):
    Type = ComponentTypes.ExternalFlow

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        ExternalBase.__init__(self, inputs['path'], col_num=1)
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # report variables
        self.flow_rate = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        self.flow_rate = self.get_value(inputs.time)
        return SimulationResponse(inputs.time, inputs.time_step, self.flow_rate, inputs.temperature)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): float(self.flow_rate)}
