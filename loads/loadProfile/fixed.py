from loads.loadProfile.base import Base


class Fixed(Base):

    def __init__(self, load):
        Base.__init__(self)

        self.load = load

    def get_load(self, time):
        return self.load
