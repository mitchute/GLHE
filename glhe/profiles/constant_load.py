from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes


class ConstantLoad(SimulationEntryPoint):
    Type = ComponentTypes.ConstantLoad

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.load = inputs['value']
        self.ip = ip
        self.op = op

        # report variables
        self.inlet_temp = ip.init_temp()
        self.outlet_temp = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse):
        self.inlet_temp = inputs.temperature
        flow_rate = inputs.flow_rate

        if flow_rate == 0:
            return inputs

        specific_heat = self.ip.props_mgr.fluid.get_cp(self.inlet_temp)
        self.outlet_temp = self.load / (flow_rate * specific_heat) + self.inlet_temp
        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): float(self.inlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): float(self.load)}
