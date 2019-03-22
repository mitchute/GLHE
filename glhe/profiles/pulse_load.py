from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse


class PulseLoad(SimulationEntryPoint):
    Type = ComponentTypes.PulseLoad

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.load = inputs['value']
        self.start_time = inputs['start-time']
        self.end_time = inputs['end-time']
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        if self.start_time <= inputs.sim_time < self.end_time:
            inlet_temp = inputs.temperature
            flow_rate = inputs.flow_rate
            specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
            self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
            return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.flow_rate, self.outlet_temp)
        else:
            self.load = 0
            return inputs

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Outlet Temp. [C]'): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Load [W]'): float(self.load)}
