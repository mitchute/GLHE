from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse


class GroundHeatExchangerLTS(SimulationEntryPoint):

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.ip = ip
        self.op = op

    def simulate_time_step(self, inputs: SimulationResponse):
        return inputs

    def report_outputs(self):
        pass

