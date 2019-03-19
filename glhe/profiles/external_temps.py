from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase


class ExternalTemps(ExternalBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        ExternalBase.__init__(self, input_file_path=inputs['path'], col_num=2)
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        self.outlet_temp = self.get_value(inputs.sim_time)
        return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.mass_flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'ExternalTemps: temperature [C]': self.outlet_temp}
