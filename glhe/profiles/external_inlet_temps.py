from typing import Union

from glhe.inputProcessor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.outputProcessor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase


class ExternalInletTemps(ExternalBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        ExternalBase.__init__(self, input_file_path=inputs['path'], col_num=2)
        self.ip = ip
        self.op = op

    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]):
        temp = self.get_value(sim_time)
        return SimulationResponse(sim_time, time_step, mass_flow_rate, temp)
