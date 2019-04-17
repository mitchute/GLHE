from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse


class SingleUTubePassThroughSegment(SimulationEntryPoint):

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, {'name': 'Seg No. {}'.format(inputs['segment-number'])})
        self.ip = ip
        self.op = op

        # report variables
        self.temperature = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass

    def report_outputs(self) -> dict:
        return {}
