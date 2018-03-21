import abc


class BoreholeBase(object):

    def __init__(self, fluid):
        pass

    # pragma: no cover
    @abc.abstractmethod
    def get_outlet_temps(self, t_in_1, t_in_2, mdot):
        pass
