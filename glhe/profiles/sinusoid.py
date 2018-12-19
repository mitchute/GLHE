from math import pi, sin

from glhe.profiles.base import Base


class Sinusoid(Base):

    def __init__(self, amplitude, offset, period):
        Base.__init__(self)

        self.amplitude = amplitude
        self.offset = offset
        self.period = period

    def get_value(self, time):
        return self.amplitude * sin(2 * pi * time / self.period) + self.offset
