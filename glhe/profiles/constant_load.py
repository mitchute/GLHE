from typing import Union

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class ConstantLoad(SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        self.load = inputs['value']
        self.ip = ip
        self.op = op

    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]):
        specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
        outlet_temp = self.load / (mass_flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(sim_time, time_step, mass_flow_rate, outlet_temp)
