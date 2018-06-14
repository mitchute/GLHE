from glhe.profiles.base import Base


class Fixed(Base):

    def __init__(self, value):
        Base.__init__(self)

        self.value = value

    def get_value(self, time=0):
        return self.value
