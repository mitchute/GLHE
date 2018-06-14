from abc import ABC, abstractmethod


class SimulationEntryPoint(ABC):

    @abstractmethod
    def simulate_time_step(self, temp, flow, time_step):
        pass
