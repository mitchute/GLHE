from abc import ABC, abstractmethod


class BoreholeBase(ABC):

    def __init__(self, fluid):
        pass  # pragma: no cover

    @abstractmethod
    def get_outlet_temps(self, t_in_1, t_in_2, m_dot):
        pass
