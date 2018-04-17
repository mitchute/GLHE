import abc


class Base(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_load(self, time):
        pass  # pragma: no cover
