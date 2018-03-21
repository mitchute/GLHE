from glhe.borehole.simpleHX import BoreholeSimpleHX
from glhe.topology.type import SegmentType


class Segment(object):

    _count = 0

    def __init__(self, segment_type):
        if segment_type == "simple":
            self._type = SegmentType.SIMPLE
            self._model = BoreholeSimpleHX(None)

            self._segment_num = Segment._count
            Segment._count += 1
