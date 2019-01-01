from glhe.topology.borehole_types import BoreholeType
from glhe.topology.pipe import Pipe
from glhe.topology.segment_base import SegmentBase


class SingleUTubeGroutedSegment(SegmentBase):

    def __init__(self, inputs, fluid_inst, grout_inst, soil_inst):

        SegmentBase.__init__(self, fluid_inst=fluid_inst, grout_inst=grout_inst, soil_inst=soil_inst)

        self.type = BoreholeType.SINGLE_U_TUBE_GROUTED

        self.fluid = fluid_inst
        self.grout = grout_inst
        self.soil = soil_inst

        self.pipe = Pipe(inputs['pipe-data'], fluid_inst=fluid_inst)

    def calc_fluid_volume(self):
        pass  # pragma: no cover

    def calc_grout_volume(self):
        pass  # pragma: no cover

    def calc_pipe_volume(self):
        pass  # pragma: no cover
