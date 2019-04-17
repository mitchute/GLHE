from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase


class ExternalTemps(ExternalBase, SimulationEntryPoint):
    Type = ComponentTypes.ExternalTemps

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        ExternalBase.__init__(self, inputs['path'], col_num=2)
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        self.outlet_temp = self.get_value(inputs.time)
        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): float(self.outlet_temp)}
