from math import pi, sin

from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes


class SinusoidLoad(SimulationEntryPoint):
    Type = ComponentTypes.SinusoidLoad

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.amplitude = inputs['amplitude']
        self.offset = inputs['offset']
        self.period = inputs['period']
        self.ip = ip
        self.op = op

        # report variables
        self.load = 0
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        flow_rate = inputs.flow_rate

        if flow_rate == 0:
            return inputs

        t = inputs.time
        dt = inputs.time_step
        inlet_temp = inputs.temperature

        self.load = self.amplitude * sin(2 * pi * (t + dt) / self.period) + self.offset
        specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
        self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): float(self.load)}
