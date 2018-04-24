from loads.bins.no_aggregation_method import NoAggMethod
from loads.bins.static_method import StaticMethod
from loads.bins.dynamic_method import DynamicMethod
from loads.bins.method_types import MethodType


class GFunction(object):

    def __init__(self, agg_method='DYNAMIC'):

        self._agg_method_name = agg_method.upper()

        if self._agg_method_name == 'DYNAMIC':
            self._agg_method = MethodType.DYNAMIC
            self._agg = DynamicMethod()
        elif self._agg_method_name == 'STATIC':
            self._agg_type = MethodType.STATIC
            self._agg = StaticMethod()
        elif self._agg_method_name == 'NONE':
            self._agg_type = MethodType.NOAGG
            self._agg = NoAggMethod
        else:
            raise ValueError("'{}' is not supported".format(self._agg_method_name))

    def simulate(self):
        self._agg.loads[0].get_load
