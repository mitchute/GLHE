from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.aggregation.no_agg_method import NoAggMethod
from glhe.aggregation.static_method import StaticMethod
from glhe.globals.functions import merge_dicts
from glhe.input_processor.input_processor import InputProcessor


def make_agg_method(inputs: dict, ip: InputProcessor):
    """
    Factory method for creating load aggregation objects

    :param inputs: load aggregation inputs
    :param ip: input processor instance
    :return: load aggregation object
    """

    method = inputs['method']
    if method == 'static':
        return StaticMethod(inputs)
    elif method == 'dynamic':
        inputs = merge_dicts(inputs, {'runtime': ip.input_dict['simulation']['runtime']})
        return DynamicMethod(inputs)
    elif method == 'none':
        return NoAggMethod()
    else:
        raise ValueError("Load aggregation method '{}' not found.".format(method))
