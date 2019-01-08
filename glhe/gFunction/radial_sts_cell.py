from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase


class RadialCell(PropertiesBase):

    def __init__(self, inputs):
        PropertiesBase.__init__(self, inputs=inputs)
        self.radius_inner = inputs['inner radius']
        self.radius_outer = self.calc_outer_radius()
        self.radius_center = self.calc_center_radius()
        self.thickness = inputs['thickness']
        self.temperature = inputs['initial temperature']
        self.prev_temperature = inputs['initial temperature']
        self.volume = self.calc_volume()

    def calc_outer_radius(self):
        return self.radius_inner + self.thickness

    def calc_center_radius(self):
        return self.radius_inner + self.thickness / 2.0

    def calc_volume(self):
        return PI * (self.radius_outer ** 2 - self.radius_inner ** 2)
