from glhe.topology.borehole import Borehole


class Path(object):

    _count = 0

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._boreholes = []

        self._path_num = Path._count
        Path._count += 1

        for borehole in inputs["boreholes"]:
            self._boreholes.append(Borehole(borehole))

    def flow_resistance(self):
        for borehole in self._boreholes:
            borehole.flow_resistance()
