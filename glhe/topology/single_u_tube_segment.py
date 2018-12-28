from glhe.topology.segment_base import SegmentBase


class SingleUTubeSegment(SegmentBase):

    def __init__(self, inputs, fluid):
        SegmentBase.__init__(self)

        # Keep reference to fluid instance here for usage
        self.fluid = fluid

    def update(self):
        pass
