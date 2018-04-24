import abc

from collections import deque


class BaseMethod(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.loads = deque()

    @abc.abstractmethod
    def add_load(self, load):
        pass  # pragma: no cover
