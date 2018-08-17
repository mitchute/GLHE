from glhe.aggregation.base_bin import BaseBin


class DynamicBin(BaseBin):

    def __init__(self, energy=0, width=0):
        BaseBin.__init__(self, energy=energy, width=width)
