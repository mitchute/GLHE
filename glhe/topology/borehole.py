from glhe.topology.segment import Segment


class Borehole(object):

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._depth = inputs["depth"]
