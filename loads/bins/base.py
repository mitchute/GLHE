import abc


class BaseBin(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):

        self._energy = 0
        self._width = 0

    @abc.abstractmethod
    def pop_one_impulse(self, timestep):
        pass

    @abc.abstractmethod
    def add_impulse(self, timestep):
        pass
