class BoreholeBase(object):

    def __init__(self, inputs):
        self.DEPTH = inputs['depth']
        self.DIAMETER = inputs['diameter']
        self.RADIUS = self.DIAMETER / 2
