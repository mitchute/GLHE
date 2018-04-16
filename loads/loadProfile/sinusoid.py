from math import sin, pi

from loads.loadProfile.base import Base


class Sinusoid(Base):

    def __init__(self, amplitude, offset, period):
        Base.__init__(self)

        self.load_amplitude = amplitude
        self.load_offset = offset
        self.period = period

    def get_load(self, time):
        return self.load_amplitude * sin(2 * pi * time / self.period) + self.load_offset
