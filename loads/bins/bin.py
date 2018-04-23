class BaseBin(object):

    def __init__(self, energy=0, width=0):
        self.energy = energy
        self.width = width

    def get_load(self):
        return self.energy / self.width
