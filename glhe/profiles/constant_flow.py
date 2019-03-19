from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class ConstantFlow(SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        self.flow_rate = inputs['value']
        self.ip = ip
        self.op = op

    def simulate_time_step(self, inputs: SimulationResponse):
        return SimulationResponse(inputs.sim_time, inputs.time_step, self.flow_rate, inputs.temperature)

    def report_outputs(self):
        return {'ConstantFlow: flow rate [kg/s]': self.flow_rate}
