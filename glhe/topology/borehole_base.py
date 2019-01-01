from abc import abstractmethod


class BoreholeBase(object):

    def __init__(self, inputs):
        self.DEPTH = inputs['depth']
        self.DIAMETER = inputs['diameter']
        self.RADIUS = self.DIAMETER / 2

    @abstractmethod
    def calc_fluid_volume(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_grout_volume(self):
        pass  # pragma: no cover

    @abstractmethod
    def calc_pipe_volume(self):
        pass  # pragma: no cover
