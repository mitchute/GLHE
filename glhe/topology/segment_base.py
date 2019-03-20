from abc import ABC, abstractmethod


class SegmentBase(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def calc_total_volume(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_fluid_volume(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_grout_volume(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_pipe_volume(self):
        pass  # pragma: no cover
