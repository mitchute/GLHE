from abc import ABC, abstractmethod


class SegmentBase(ABC):

    @abstractmethod
    def update(self):
        pass
