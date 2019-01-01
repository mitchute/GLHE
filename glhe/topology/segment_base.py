from abc import ABC, abstractmethod


class SegmentBase(ABC):

    def __init__(self, fluid_inst=None, grout_inst=None, soil_inst=None):
        self.fluid = fluid_inst
        self.grout = grout_inst
        self.soil = soil_inst

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
