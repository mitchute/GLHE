from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor

from glhe.output_processor.report_types import ReportTypes


class ConstantTemp(SimulationEntryPoint):
    Type = ComponentTypes.ConstantTemp

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.temperature = inputs['value']
        self.ip = ip
        self.op = op

        self.inlet_temperature = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse):
        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.temperature)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.temperature}
