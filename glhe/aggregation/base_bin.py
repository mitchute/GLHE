class BaseBin(object):

    def __init__(self, energy=0, width=0):
        """
        Base bin that stores the energy and time-span use to describe the load

        :param energy: Energy stored [J]
        :param width: Time-span of load [s]
        """

        self.energy = energy
        self.width = width

    def get_load(self):
        return self.energy / self.width
