from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase


class RadialCell(PropertiesBase):

    def __init__(self, inputs, half_cell=False):
        PropertiesBase.__init__(self, inputs=inputs)

        self.type = inputs['type']
        self.radius_inner = inputs['inner radius']
        self.thickness = inputs['thickness']
        self.temperature = inputs['initial temperature']
        self.prev_temperature = inputs['initial temperature']

        if half_cell:
            self.radius_center = self.radius_inner

        else:
            self.radius_outer = self.radius_inner + self.thickness
            self.radius_center = self.radius_inner + self.thickness / 2.0

        self.volume = self.calc_volume()

    def calc_volume(self):
        return PI * (self.radius_outer ** 2 - self.radius_inner ** 2)
