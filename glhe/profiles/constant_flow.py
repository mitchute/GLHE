from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor

from glhe.output_processor.report_types import ReportTypes


class ConstantFlow(SimulationEntryPoint):
    Type = ComponentTypes.ConstantFlow

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.flow_rate = inputs['value']
        self.ip = ip
        self.op = op

    def simulate_time_step(self, inputs: SimulationResponse):
        return SimulationResponse(inputs.time, inputs.time_step, self.flow_rate, inputs.temperature)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): float(self.flow_rate)}
