from glhe.globals.functions import merge_dicts
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class Path(object):

    def __init__(self, inputs, ip, op):

        # input processor
        self.ip = ip

        # output processor
        self.op = op

        self.name = inputs["name"]

        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        # Initialize boreholes
        self.boreholes = []
        for borehole in inputs["boreholes"]:
            self.boreholes.append(SingleUTubeGroutedBorehole(merge_dicts(borehole,
                                                                         {'initial temp': inputs['initial temp']}),
                                                             self.ip,
                                                             self.op))

        # Initialize other parameters
        self.mass_flow_rate = 0
        self.flow_resistance = 0

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
