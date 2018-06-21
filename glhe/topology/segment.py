from glhe.borehole.simpleHX import BoreholeSimpleHX
from glhe.topology.segment_types import SegmentType


class Segment(object):
    _count = 0

    def __init__(self, segment_type, fluid):
        # Initialize segment
        if segment_type == "simple":
            self._type = SegmentType.SIMPLE
            self._model = BoreholeSimpleHX(None)

        # Keep reference to fluid instance here for usage
        self._fluid = fluid

        # Track segment number
        self._segment_num = Segment._count
        Segment._count += 1
