from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase


class PipeBase(PropertiesBase):

    def __init__(self, inputs):

        PropertiesBase.__init__(self, inputs=inputs)

        self.INNER_DIAMETER = inputs["inner diameter"]
        self.OUTER_DIAMETER = inputs["outer diameter"]
        self.LENGTH = inputs['length']
        self.INIT_TEMP = inputs['initial temp']

        self.THICKNESS = (self.OUTER_DIAMETER - self.INNER_DIAMETER) / 2
        self.INNER_RADIUS = self.INNER_DIAMETER / 2
        self.OUTER_RADIUS = self.OUTER_DIAMETER / 2

        self.AREA_CR_INNER = PI / 4 * self.INNER_DIAMETER ** 2
        self.AREA_CR_OUTER = PI / 4 * self.OUTER_DIAMETER ** 2
        self.AREA_CR_PIPE = self.AREA_CR_OUTER - self.AREA_CR_INNER

        self.AREA_S_INNER = PI * self.INNER_DIAMETER * self.LENGTH
        self.AREA_S_OUTER = PI * self.OUTER_DIAMETER * self.LENGTH

        self.FLUID_VOL = self.AREA_CR_INNER * self.LENGTH
        self.TOTAL_VOL = self.AREA_CR_OUTER * self.LENGTH
        self.WALL_VOL = self.AREA_CR_PIPE * self.LENGTH
