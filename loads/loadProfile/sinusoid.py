from loads.loadProfile.base import Base


class SingleImpulse(Base):

    def __init__(self, load_amplitude, period):
        Base.__init__(self)

        self.load_amplitude = load_amplitude
        self.period = period

    def get_load(self, time):
        pass
