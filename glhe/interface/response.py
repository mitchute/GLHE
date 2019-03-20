class SimulationResponse(object):
    def __init__(self, sim_time, time_step, flow_rate, temperature):
        self.sim_time = sim_time
        self.time_step = time_step
        self.flow_rate = flow_rate
        self.temperature = temperature
