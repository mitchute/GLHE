class BaseBin(object):

    def __init__(self, energy=0, width=0):
        self.energy = energy
        self.width = width
        self.g = 0
        self.g_fixed = False

    def get_load(self):
        try:
            return self.energy / self.width
        except ZeroDivisionError:
            return 0
