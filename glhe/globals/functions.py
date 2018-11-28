import json
from math import exp, factorial

from glhe.globals.constants import SEC_IN_HOUR


def smoothing_function(x, a, b):
    """
    Sigmoid smoothing function

    https://en.wikipedia.org/wiki/Sigmoid_function

    :param x: independent variable
    :param a: fitting parameter 1
    :param b: fitting parameter 2
    :return: float between 0-1
    """

    return 1 / (1 + exp(-(x - a) / b))


def temp_in_kelvin(x):
    """
    Converts Celsius to Kelvin

    :param x: temperature in Celsius
    :return: temperature in Kelvin
    """

    return x + 273.15


def set_time_step(input_time_step_per_hour):
    """
    Converts the input time-steps per hour to the nearest possible time-step in seconds.
    Time-step should be evenly divisible into an hour.

    :param input_time_step_per_hour:
    :return:
    """
    try:
        input_time_step = int(SEC_IN_HOUR / input_time_step_per_hour)
    except ZeroDivisionError:
        raise ZeroDivisionError("Incorrect times-step specified")

    time_step_per_hour = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
    time_step_list = [int(SEC_IN_HOUR / x) for x in time_step_per_hour]

    if input_time_step in time_step_list:
        return int(input_time_step)
    else:
        # We should probably raise some warning here
        # Need to think about adding some logging features eventually
        return int(min(time_step_list, key=lambda x: abs(x - input_time_step)))


def load_json(path):
    """
    Loads a json file

    :param path: file path
    :return: loaded json object as parsed dict object
    """

    with open(path, 'r') as f:
        json_blob = f.read()
    return json.loads(json_blob)


def write_json(path, obj):
    with open(path, 'w') as f:
        f.write(json.dumps(obj,
                           sort_keys=True,
                           indent=2,
                           separators=(',', ': ')))


def hanby(time, vol_flow_rate, volume):
    """
    Computes the non-dimensional response of a fluid conduit
    assuming well mixed nodes. The model accounts for the thermal
    capacity of the fluid and diffusive mixing.

    Hanby, V.I., J.A. Wright, D.W. Fetcher, D.N.T. Jones. 2002
    'Modeling the dynamic response of conduits.' HVAC&R Research 8(1): 1-12.

    The model is non-dimensional, so input parameters should have consistent units
    for that are able to compute the non-dimensional time parameter, tau.

    :param time: time of fluid response
    :param vol_flow_rate: volume flow rate
    :param volume: volume of fluid circuit
    :return:
    """

    tau = vol_flow_rate * time / volume
    # tau = max(1/0.7 * tau - 0.9285, 0)
    num_nodes = 46
    ret_sum = 1
    for i in range(1, num_nodes):
        ret_sum += (num_nodes * tau) ** i / factorial(i)

    return 1 - exp(-num_nodes * tau) * ret_sum


def merge_dicts(d, d_append):
    """
    Return new dictionary with d_append added to d at the root level

    :param d: input dictionary
    :param d_append: dictionary to append
    :return: combined dict
    """

    return {**d, **d_append}
