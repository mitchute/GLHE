from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse

class ImpulseLoad(SimulationEntryPoint):

    def __init__(self, inputs, ip, op):

        self.load = load_value
        self.start_time = start_time
        self.end_time = end_time

        self.ip = ip
        self.op = op

    def simulate_time_step(self, sim_time, time_step, mass_flow_rate, inlet_temp):
        if self.start_time <= sim_time < self.end_time:
            return self.load
        else:
            return 0
