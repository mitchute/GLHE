from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse

from glhe.output_processor.report_types import ReportTypes


class PulseLoad(SimulationEntryPoint):
    Type = ComponentTypes.PulseLoad

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.load = inputs['value']
        self.start_time = inputs['start-time']
        self.end_time = inputs['end-time']
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        if self.start_time <= inputs.time < self.end_time:
            flow_rate = inputs.flow_rate

            if flow_rate == 0:
                return inputs

            inlet_temp = inputs.temperature

            specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
            self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
            return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)
        else:
            self.load = 0
            return inputs

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): float(self.load)}
