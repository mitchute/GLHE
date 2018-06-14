from loads.profiles.base import Base


class Impulse(Base):

    def __init__(self, value, start_time, end_time):
        Base.__init__(self)

        self.value = value
        self.start_time = start_time
        self.end_time = end_time

    def get_value(self, time):
        if self.start_time <= time < self.end_time:
            return self.value
        else:
            return 0
