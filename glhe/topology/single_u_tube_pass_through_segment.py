from glhe.functions import init_temp
from glhe.topology.single_u_tube_grouted_segment import TimeStepStructure


class SingleUTubePassThroughSegment(object):
    def __init__(self):
        self.temperature = init_temp()

    def get_outlet_2_temp(self):
        return self.temperature

    def simulate_time_step(self, _, inputs: TimeStepStructure):
        self.temperature = inputs.inlet_temp_1
