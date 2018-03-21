from glhe.properties.base import PropertiesBase
from glhe.properties.pipe import Pipe
from glhe.topology.segment import Segment


class Borehole(object):

    _count = 0

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._depth = inputs["depth"]
        self._diameter = inputs["diameter"]
        self._grout = PropertiesBase(conductivity=inputs["grout"]["conductivity"],
                                     density=inputs["grout"]["density"],
                                     specific_heat=inputs["grout"]["specific heat"])
        self._pipe = Pipe(conductivity=inputs["pipe"]["conductivity"],
                          density=inputs["pipe"]["density"],
                          specific_heat=inputs["pipe"]["specific heat"],
                          inner_diameter=inputs["pipe"]["inner diameter"],
                          outer_diameter=inputs["pipe"]["outer diameter"])

        self._bh_num = Borehole._count
        Borehole._count += 1

        self._segments = []
        for segment in range(inputs["segments"]):
            self._segments.append(Segment(segment_type=inputs["type"]))

    def flow_resistance(self):
        pass

    @staticmethod
    def friction_factor():
        pass