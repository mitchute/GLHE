from abc import ABC, abstractmethod


class SimulationEntryPoint(ABC):

    @abstractmethod
    def simulate_time_step(self, sim_time, time_step, mass_flow_rate, inlet_temp):
        pass  # pragma: no cover
