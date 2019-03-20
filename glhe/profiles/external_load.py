from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase


class ExternalLoad(ExternalBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        path = inputs['path']
        ExternalBase.__init__(self, input_file_path=path, col_num=0)
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
        return {'ExternalLoad: temperature [C]': self.outlet_temp,
                'ExternalLoad: load [W]': self.load}
