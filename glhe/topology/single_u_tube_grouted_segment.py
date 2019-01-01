from glhe.globals.constants import PI
from glhe.globals.functions import merge_dicts
from glhe.topology.borehole_types import BoreholeType
from glhe.topology.pipe import Pipe
from glhe.topology.segment_base import SegmentBase


class SingleUTubeGroutedSegment(SegmentBase):

    def __init__(self, inputs, fluid_inst, grout_inst, soil_inst):

        SegmentBase.__init__(self, fluid_inst=fluid_inst, grout_inst=grout_inst, soil_inst=soil_inst)

        self.type = BoreholeType.SINGLE_U_TUBE_GROUTED

        self.NUM_PIPES = 2

        self.fluid = fluid_inst
        self.grout = grout_inst
        self.soil = soil_inst

        self.LENGTH = inputs['length']
        self.DIAMETER = inputs['diameter']

        self.pipe_1 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.LENGTH,
                                                             'initial temp': inputs['initial temp']}),
                           fluid_inst=fluid_inst)

        self.pipe_2 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.LENGTH,
                                                             'initial temp': inputs['initial temp']}),
                           fluid_inst=fluid_inst)

        self.TOTAL_VOL = self.calc_total_volume()
        self.FLUID_VOL = self.calc_fluid_volume()
        self.GROUT_VOL = self.calc_grout_volume()
        self.PIPE_VOL = self.calc_pipe_volume()

    def calc_total_volume(self):
        return PI / 4 * self.DIAMETER ** 2 * self.LENGTH

    def calc_fluid_volume(self):
        return self.pipe_1.FLUID_VOL + self.pipe_2.FLUID_VOL

    def calc_grout_volume(self):
        return self.calc_total_volume() - self.pipe_1.TOTAL_VOL - self.pipe_2.TOTAL_VOL

    def calc_pipe_volume(self):
        return self.pipe_1.PIPE_WALL_VOL + self.pipe_2.PIPE_WALL_VOL
