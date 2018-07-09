import json
from math import exp

from numpy import array


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


def set_time_step(input_time_step):
    """
    Converts the input time-step in seconds to the nearest possible time-step.
    Time-step should be evenly divisible into an hour.

    :param input_time_step:
    :return:
    """

    time_step_per_hour = array([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])
    time_step_list = 3600 / time_step_per_hour

    if input_time_step in time_step_list:
        return input_time_step
    else:
        # We should probably raise some warning here
        # Need to think about adding some logging features eventually
        return min(time_step_list, key=lambda x: abs(x - input_time_step))


def load_json(path):
    """
    Loads a json file

    :param path: file path
    :return: loaded json object as parsed dict object
    """

    with open(path) as f:
        json_blob = f.read()
    return json.loads(json_blob)
