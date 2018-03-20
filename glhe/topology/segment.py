from glhe.borehole.simpleHX import BoreholeSimpleHX
from glhe.topology.type import SegmentType


class Segment(object):

    def __init__(self, segment_type):
        if segment_type == "simple":
            self._type = SegmentType.SIMPLE
            self._model = BoreholeSimpleHX(None)
