from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
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
        self.load = self.get_value(inputs.sim_time)
        inlet_temp = inputs.temperature
        flow_rate = inputs.flow_rate
        specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
        self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Outlet Temp. [C]'): float(self.outlet_temp),
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Load [W]'): float(self.load)}
