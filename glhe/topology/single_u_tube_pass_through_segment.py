from glhe.topology.segment_base import SegmentBase


class SingleUTubePassThroughSegment(SegmentBase):

    def __init__(self, inputs):
        SegmentBase.__init__(self, ip=None, op=None)
        self.temp = inputs['initial temp']

    def calc_total_volume(self):
        return 0

    def calc_fluid_volume(self):
        return 0

    def calc_grout_volume(self):
        return 0

    def calc_pipe_volume(self):
        return 0

    def simulate(self, _, **kwargs):
        self.temp = kwargs['inlet 1 temp']

    def get_outlet_1_temp(self):
        return self.temp

    def get_outlet_2_temp(self):
        return self.temp
