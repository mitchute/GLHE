from glhe.aggregation.base_bin import BaseBin


class StaticBin(BaseBin):

    def __init__(self, energy=0, width=0):
        BaseBin.__init__(self, energy=energy, width=width)

    def merge(self, bins):
        if isinstance(bins, StaticBin):
            bins = [bins]
        for cur_bin in bins:
            self.energy += cur_bin.energy
            self.width += cur_bin.width
