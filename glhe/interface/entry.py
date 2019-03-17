from abc import ABC, abstractmethod
from typing import Union

from glhe.interface.response import SimulationResponse


class SimulationEntryPoint(ABC):

    @abstractmethod
    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]) -> SimulationResponse:
        pass  # pragma: no cover
