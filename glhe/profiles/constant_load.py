from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class ConstantLoad(SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        self.load = inputs['value']
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, inputs: SimulationResponse):
        inlet_temp = inputs.temperature
        flow_rate = inputs.mass_flow_rate
        specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
        self.outlet_temp = self.load / (flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.mass_flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'ConstantLoad: temperature [C]': self.outlet_temp,
                'ConstantLoad: load [W]': self.load}
