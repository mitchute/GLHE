from glhe.topology.borehole import Borehole


class Path(object):

    _count = 0

    def __init__(self, inputs):

        # Get inputs from json blob
        self._name = inputs["name"]
        self._boreholes = []

        for borehole in inputs["boreholes"]:
            self._boreholes.append(Borehole(borehole))

        self.mass_flow_fraction = 0
        self.mass_flow_rate = 0

        # Get constant part of pipe pressure loss equation
        self.const_flow_resistance = 0
        for bh in self._boreholes:
            self.const_flow_resistance += bh.const_flow_resistance

        # track path number
        self._path_num = Path._count
        Path._count += 1

    def flow_resistance(self):
        sum_resistance = 0
        for borehole in self._boreholes:
            sum_resistance += borehole.flow_resistance()
        return sum_resistance

    def set_flow_rate(self, mass_flow_fraction, mass_flow_rate):
        self.mass_flow_fraction = mass_flow_fraction
        self.mass_flow_rate = mass_flow_rate
        for bh in self._boreholes:
            bh.set_flow_rate(mass_flow_rate)

