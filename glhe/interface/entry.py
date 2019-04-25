from abc import ABC, abstractmethod

from glhe.interface.response import SimulationResponse


class SimulationEntryPoint(ABC):  # pragma: no cover

    def __init__(self, inputs: dict):  # pragma: no cover
        try:  # pragma: no cover
            self.name = inputs['name'].upper()
        except KeyError:  # pragma: no cover
            pass  # pragma: no cover

    @abstractmethod  # pragma: no cover
    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass  # pragma: no cover

    @abstractmethod  # pragma: no cover
    def report_outputs(self) -> dict:
        pass  # pragma: no cover
