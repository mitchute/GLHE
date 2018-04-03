from glhe.topology.borehole import Borehole


class Path(object):

    _count = 0

    def __init__(self, inputs, fluid_instance):

        # Get inputs from json blob
        self._name = inputs["name"]

        # Keep reference to fluid instance for usage
        self._fluid = fluid_instance

        # Initialize boreholes
        self._boreholes = []
        for borehole in inputs["boreholes"]:
            self._boreholes.append(Borehole(borehole, fluid_instance=self._fluid))

        # Initialize other parameters
        self._mass_flow_rate = 0

        # Track path number
        self._path_num = Path._count
        Path._count += 1

    def get_flow_resistance(self):
        sum_resistance = 0
        for borehole in self._boreholes:
            sum_resistance += borehole.get_flow_resistance()
        return sum_resistance

    def set_mass_flow_rate(self, mass_flow_rate):
        self._mass_flow_rate = mass_flow_rate
        for bh in self._boreholes:
            bh.set_flow_rate(mass_flow_rate)
