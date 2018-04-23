from loads.profiles.base import Base


class External(Base):

    def __init__(self, path):
        Base.__init__(self)
        pass

    def get_load(self, time=0):
        pass
