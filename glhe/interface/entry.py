from abc import ABC, abstractmethod

from glhe.interface.response import SimulationResponse


class SimulationEntryPoint(ABC):

    def __init__(self, name):
        try:
            self.name = name.upper()
        except KeyError:
            pass

    @abstractmethod
    def simulate_time_step(self, response: SimulationResponse) -> SimulationResponse:
        pass  # pragma: no cover

    @abstractmethod
    def report_outputs(self) -> dict:
        pass  # pragma: no cover
