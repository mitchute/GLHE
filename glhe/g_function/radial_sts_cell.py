from math import pi


class RadialCell(object):

    def __init__(self, inputs):
        self.type = inputs['type']

        self.inner_radius = inputs['inner radius']
        self.center_radius = inputs['center radius']
        self.outer_radius = inputs['outer radius']

        self.thickness = inputs['thickness']

        self.temperature = inputs['initial temperature']
        self.prev_temperature = inputs['initial temperature']

        self.conductivity = inputs['conductivity']
        self.rho_cp = inputs['vol heat capacity']

        self.volume = self.calc_volume()

    def calc_volume(self):
        return pi * (self.outer_radius ** 2 - self.inner_radius ** 2)
