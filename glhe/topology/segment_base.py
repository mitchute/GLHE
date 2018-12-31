from abc import ABC, abstractmethod


class SegmentBase(ABC):

    @abstractmethod
    def update(self):
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
