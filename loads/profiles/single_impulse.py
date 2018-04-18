from loads.profiles.base import Base


class SingleImpulse(Base):

    def __init__(self, load, start_time, end_time):
        Base.__init__(self)

        self.load = load
        self.start_time = start_time
        self.end_time = end_time

    def get_load(self, time):
        if self.start_time <= time < self.end_time:
            return self.load
        else:
            return 0
