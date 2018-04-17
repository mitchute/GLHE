import abc


class BoreholeBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, fluid):
        pass

    @abc.abstractmethod
    def get_outlet_temps(self, t_in_1, t_in_2, m_dot):
        pass
