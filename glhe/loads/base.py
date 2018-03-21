import abc


class LoadAggregationBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def store_load(self, load, time):
        pass

    # pragma: no cover
    @abc.abstractmethod
    def get_load(self, time):
        pass
