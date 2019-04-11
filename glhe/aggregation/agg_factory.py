from glhe.aggregation.dynamic import Dynamic
from glhe.aggregation.no_agg import NoAgg
from glhe.aggregation.static import Static
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
        return Static(inputs)
    elif method == 'dynamic':
        inputs = merge_dicts(inputs, {'runtime': ip.input_dict['simulation']['runtime']})
        return Dynamic(inputs)
    elif method == 'none':
        return NoAgg(inputs)
    else:
        raise ValueError("Load aggregation method '{}' is not valid.".format(method))
