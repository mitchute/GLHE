from math import pi

from glhe.properties.base import PropertiesBase


class PipeBase(PropertiesBase):

    def __init__(self, inputs):
        PropertiesBase.__init__(self, inputs=inputs)

        self.inner_diameter = inputs["inner diameter"]
        self.outer_diameter = inputs["outer diameter"]
        self.length = inputs['length']
        self.init_temp = inputs['initial temp']

        self.wall_thickness = (self.outer_diameter - self.inner_diameter) / 2
        self.inner_radius = self.inner_diameter / 2
        self.outer_radius = self.outer_diameter / 2

        self.area_cr_inner = pi / 4 * self.inner_diameter ** 2
        self.area_cr_outer = pi / 4 * self.outer_diameter ** 2
        self.area_cr_pipe = self.area_cr_outer - self.area_cr_inner

        self.area_s_inner = pi * self.inner_diameter * self.length
        self.area_s_outer = pi * self.outer_diameter * self.length

        self.total_vol = self.area_cr_outer * self.length
        self.fluid_vol = self.area_cr_inner * self.length
        self.pipe_wall_vol = self.area_cr_pipe * self.length
