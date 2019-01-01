from glhe.globals.functions import merge_dicts
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class Path(object):

    def __init__(self, inputs, fluid_inst, soil_inst):

        # Get inputs from json blob
        self.NAME = inputs["name"]

        # Keep reference to instance for usage
        self.fluid = fluid_inst
        self.soil = soil_inst

        # Initialize boreholes
        self.boreholes = []
        for borehole in inputs["boreholes"]:
            self.boreholes.append(SingleUTubeGroutedBorehole(merge_dicts(borehole['borehole-data'],
                                                                         {'initial temp': inputs['initial temp']}),
                                                             fluid_inst=fluid_inst,
                                                             soil_inst=soil_inst))

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
