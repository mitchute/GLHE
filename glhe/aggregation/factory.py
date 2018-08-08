from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.aggregation.no_aggregation_method import NoAggMethod
from glhe.aggregation.static_method import StaticMethod


def load_agg_factory(inputs):
    """
    Factory method for creating load aggregation objects

    :param inputs: json blob from inputs
    :return: load aggregation object
    """

    load_agg_type = inputs['type']
    if load_agg_type == 'static':
        try:
            return StaticMethod(inputs['static'])
        except KeyError:
            return StaticMethod()
    elif load_agg_type == 'dynamic':
        try:
            return DynamicMethod(inputs['dynamic'])
        except KeyError:
            return StaticMethod()
    elif load_agg_type == 'none':
        return NoAggMethod()
    else:
        raise ValueError("'{}' aggregation type is not supported".format(load_agg_type))
