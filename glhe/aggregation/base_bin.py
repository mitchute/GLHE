class BaseBin(object):

    def __init__(self, energy=0, width=0, abs_time=0):
        self.energy = energy
        self.width = width
        self.abs_time = abs_time

    def get_load(self):
        try:
            return self.energy / self.width
        except ZeroDivisionError:
            return 0
