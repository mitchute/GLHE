import abc


class Base(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_load(self, time):
        pass  # pragma: no cover
