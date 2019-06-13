class SimulationResponse(object):
    def __init__(self, time: float, time_step: float, flow_rate: float, temperature: float,
                 bh_wall_temp: float = None, hp_src_heat_rate: float = None):
        self.time = time
        self.time_step = time_step
        self.flow_rate = flow_rate
        self.temperature = temperature

        if bh_wall_temp:
            self.bh_wall_temp = bh_wall_temp

        if hp_src_heat_rate:
            self.hp_src_heat_rate = hp_src_heat_rate
