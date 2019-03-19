from typing import Union

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase


class ExternalFlow(ExternalBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        path = inputs['path']
        ExternalBase.__init__(self, path, col_num=1)
        self.ip = ip
        self.op = op

        # report variables
        self.flow_rate = 0

    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]):
        self.flow_rate = self.get_value(sim_time)
        return SimulationResponse(sim_time, time_step, self.flow_rate, inlet_temp)

    def report_outputs(self):
        return {'ExternalFlow: flow rate [kg/s]': self.flow_rate}
