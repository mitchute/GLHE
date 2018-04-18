from loads.bins.base import BaseBin


class DynamicBin(BaseBin):

    def __init__(self):
        BaseBin.__init__(self)
        pass

    def pop_one_impulse(self, timestep):
        pass

    def add_impulse(self, timestep):
        pass
