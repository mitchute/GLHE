class SimulationResponse(object):
    def __init__(self, time: float, time_step: float, flow_rate: float, temperature: float, bh_wall_temp: float = None):
        self.time = time
        self.time_step = time_step
        self.flow_rate = flow_rate
        self.temperature = temperature

        if bh_wall_temp:
            self.bh_wall_temp = bh_wall_temp
