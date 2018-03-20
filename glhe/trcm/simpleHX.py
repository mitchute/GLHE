from glhe.trcm.base import TRCMBase


class TRCMSimpleHX(TRCMBase):

    def __init__(self, fluid, effectiveness=0.5):
        TRCMBase.__init__(self, fluid)
        self._fluid = fluid
        self._effectiveness = effectiveness

    def get_outlet_temps(self, t_in_1, t_in_2, mdot):
        t_out_1 = self._effectiveness * (t_in_2 - t_in_1) + t_in_1
        t_out_2 = t_in_2 - self._effectiveness * (t_in_2 - t_in_1)

        return t_out_1, t_out_2
