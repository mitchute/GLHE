from glhe.topology.borehole_types import BoreholeType
from glhe.topology.segment_base import SegmentBase


class SingleUTubeSegment(SegmentBase):

    def __init__(self, inputs, fluid):
        SegmentBase.__init__(self)

        self.type = BoreholeType.SINGLE_U_TUBE_GROUTED
        self.fluid = fluid

    def update(self):
        pass  # pragma: no cover

    def calc_fluid_volume(self):
        pass  # pragma: no cover

    def calc_grout_volume(self):
        pass  # pragma: no cover

    def calc_pipe_volume(self):
        pass  # pragma: no cover
