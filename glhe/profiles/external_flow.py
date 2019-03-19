from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase


class ExternalFlow(ExternalBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        path = inputs['path']
        ExternalBase.__init__(self, path, col_num=1)
        self.ip = ip
        self.op = op

        # report variables
        self.flow_rate = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        self.flow_rate = self.get_value(inputs.sim_time)
        return SimulationResponse(inputs.sim_time, inputs.time_step, self.flow_rate, inputs.temperature)

    def report_outputs(self):
        return {'ExternalFlow: flow rate [kg/s]': self.flow_rate}
