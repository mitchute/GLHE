from math import pi, sin
from typing import Union

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.base_load import BaseLoad


class SinusoidLoad(BaseLoad, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        BaseLoad.__init__(self)
        self.amplitude = inputs['amplitude']
        self.offset = inputs['offset']
        self.period = inputs['period']
        self.ip = ip
        self.op = op

        # report variables
        self.load = 0
        self.outlet_temp = 0

    def get_value(self, time):
        return self.amplitude * sin(2 * pi * time / self.period) + self.offset

    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]):
        self.load = self.get_value(sim_time)
        specific_heat = self.ip.props_mgr.fluid.get_cp()
        self.outlet_temp = self.load / (mass_flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(sim_time, time_step, mass_flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {'SinusoidLoad: temperature [C]': self.outlet_temp,
                'SinusoidLoad: load [W]': self.load}
