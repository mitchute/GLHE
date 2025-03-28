from abc import ABC, abstractmethod


class SimulationResponse:
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


class SimulationEntryPoint(ABC):  # pragma: no cover

    def __init__(self, inputs: dict):  # pragma: no cover
        try:  # pragma: no cover
            self.name = inputs['name'].upper()
        except KeyError:  # pragma: no cover
            pass  # pragma: no cover

    @abstractmethod  # pragma: no cover
    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass  # pragma: no cover
