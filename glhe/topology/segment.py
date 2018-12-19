from glhe.borehole.simpleHX import BoreholeSimpleHX
from glhe.topology.segment_types import SegmentType


class Segment(object):
    _count = 0

    def __init__(self, model_type, fluid):
        # Initialize segment
        if model_type == "simple":
            self.type = SegmentType.SIMPLE
            self.model = BoreholeSimpleHX(None)

        # Keep reference to fluid instance here for usage
        self.fluid = fluid

        # Track segment number
        self.segment_num = Segment._count
        Segment._count += 1
