from glhe.topology.segment_base import SegmentBase
from glhe.topology.segment_types import SegmentType


class SingleUTubeSegment(SegmentBase):

    def __init__(self, inputs, fluid):
        SegmentBase.__init__(self)

        self.type = SegmentType.SINGLE_U_TUBE
        self.fluid = fluid

    def update(self):
        pass  # pragma: no cover
