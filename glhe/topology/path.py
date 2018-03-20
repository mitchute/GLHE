from glhe.topology.borehole import Borehole


class Path(object):

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._boreholes = []
        for borehole in inputs["boreholes"]:
            self._boreholes.append(Borehole(borehole))
