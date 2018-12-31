from glhe.globals.functions import merge_dicts
from glhe.topology.single_u_tube_borehole import SingleUTubeBorehole


class Path(object):
    _count = 0

    def __init__(self, inputs, fluid, soil):

        # Get inputs from json blob
        self.NAME = inputs["name"]

        # Keep reference to instance for usage
        self.fluid = fluid
        self.soil = soil

        # Initialize boreholes
        self.boreholes = []
        for borehole in inputs["boreholes"]:
            self.boreholes.append(SingleUTubeBorehole(merge_dicts(borehole['borehole-data'],
                                                                  {'initial temp': inputs['initial temp']}),
                                                      fluid=fluid,
                                                      soil=soil))

        # Initialize other parameters
        self.mass_flow_rate = 0
        self.flow_resistance = 0

        # Track path number
        self._path_num = Path._count
        Path._count += 1

    def set_flow_resistance(self):
        self.flow_resistance = 0
        for borehole in self.boreholes:
            self.flow_resistance += borehole.get_flow_resistance()

    def set_mass_flow_rate(self, mass_flow_rate):
        self.mass_flow_rate = mass_flow_rate
        for bh in self.boreholes:
            bh.set_flow_rate(mass_flow_rate)

    def simulate(self, inlet_temperature):
        pass
