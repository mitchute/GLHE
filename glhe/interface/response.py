class SimulationResponse(object):
    def __init__(self, sim_time: float, time_step: float, flow_rate: float, temperature: float):
        self.sim_time = sim_time
        self.time_step = time_step
        self.flow_rate = flow_rate
        self.temperature = temperature
