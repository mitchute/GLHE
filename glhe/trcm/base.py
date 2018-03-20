import abc


class TRCMBase(object):

    def __init__(self, fluid):
        pass

    @abc.abstractmethod
    def get_outlet_temps(self, t_in_1, t_in_2, mdot):
        pass
