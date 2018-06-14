from abc import ABC, abstractmethod


class SimulationEntryPoint(ABC):

    @abstractmethod
    def simulate(self, temp, flow, time):
        pass
