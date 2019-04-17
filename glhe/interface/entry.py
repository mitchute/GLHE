from abc import ABC, abstractmethod

from glhe.interface.response import SimulationResponse


class SimulationEntryPoint(ABC):

    def __init__(self, inputs: dict):
        try:
            self.name = inputs['name']
        except KeyError:
            pass

    @abstractmethod
    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass  # pragma: no cover

    @abstractmethod
    def report_outputs(self) -> dict:
        pass  # pragma: no cover
