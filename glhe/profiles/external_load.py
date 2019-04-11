from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase


class ExternalLoad(ExternalBase, SimulationEntryPoint):
    Type = ComponentTypes.ExternalLoad

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        ExternalBase.__init__(self, inputs['path'], col_num=0)
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.ip = ip
        self.op = op

        # report variables
        self.load = 0
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        self.load = self.get_value(inputs.time)
        inlet_temp = inputs.temperature
        flow_rate = inputs.flow_rate
        specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
        try:
            self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
            return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)
        except ZeroDivisionError:
            return inputs

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): float(self.load)}
