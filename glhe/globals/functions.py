import json
from math import exp, factorial

import numpy as np

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

    Hanby, V.I., J.A. Wright, D.W. Fetcher, D.N.T. Jones. 2002.
    'Modeling the dynamic response of conduits.' HVAC&R Research 8(1): 1-12.

    The model is non-dimensional, so input parameters should have consistent units
    for that are able to compute the non-dimensional time parameter, tau.

    :param time: time of fluid response
    :param vol_flow_rate: volume flow rate
    :param volume: volume of fluid circuit
    :return:
    """

    tau = vol_flow_rate * time / volume
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


def runge_kutta_fourth_xy(rhs, h, x, y):
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects both x and y variables.

    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.

    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g dy/dx = f(x, y))
    :param h: step size
    :param x: step dimension
    :param y: output dimension
    :return:
    """

    k_1 = rhs(x, y)
    k_2 = rhs(x + h / 2.0, y + k_1 / 2.0)
    k_3 = rhs(x + h / 2.0, y + k_2 / 2.0)
    k_4 = rhs(x + h, y + k_3)

    return y + (k_1 + 2 * (k_2 + k_3) + k_4) / 6.0 * h


def runge_kutta_fourth_x(rhs, h, x, y):
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects only the x variable.

    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.

    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g dy/dx = f(x))
    :param h: step size
    :param x: step dimension
    :param y: output dimension
    :return:
    """

    k_1 = rhs(x)
    k_2 = rhs(x + h / 2.0)
    k_3 = rhs(x + h / 2.0)
    k_4 = rhs(x + h)

    return y + (k_1 + 2 * (k_2 + k_3) + k_4) / 6.0 * h


def runge_kutta_fourth_y(rhs, h, y):
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects only the y variable.

    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.

    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g dy/dx = f(y))
    :param h: step size
    :param y: output dimension
    :return:
    """

    k_1 = rhs(y)
    k_2 = rhs(y + k_1 / 2.0)
    k_3 = rhs(y + k_2 / 2.0)
    k_4 = rhs(y + k_3)

    return y + (k_1 + 2 * (k_2 + k_3) + k_4) / 6.0 * h


def tdma_1(a, b, c, d):
    """
    Tri-diagonal matrix solver

    This solver expects the ghost points at a(0) and c(n) be **eliminated**.

    len(b) = len(d)
    len(a) = len(c) = len(d) - 1

    Taken from: https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9

    :param a: west diagonal vector from coefficient matrix
    :param b: center diagonal vector from coefficient matrix
    :param c: east diagonal vector from coefficient matrix
    :param d: column vector
    :return: solution vecto
    """
    nf = len(d)  # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d))  # copy arrays
    for it in range(1, nf):
        mc = ac[it - 1] / bc[it - 1]
        bc[it] = bc[it] - mc * cc[it - 1]
        dc[it] = dc[it] - mc * dc[it - 1]

    xc = bc
    xc[-1] = dc[-1] / bc[-1]

    for il in range(nf - 2, -1, -1):
        xc[il] = (dc[il] - cc[il] * xc[il + 1]) / bc[il]

    return xc


def tdma_2(a, b, c, d):
    """
    Tri-diagonal matrix solver

    This solver expects the ghost points at a(0) and c(n) be **present**.

    a(0) = 0
    c(n) = 0

    len(a) = len(b) = len(c) = len(d)

    Adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Linear_Algebra/Tridiagonal_matrix_algorithm#C++
    :param a: west diagonal vector from coefficient matrix
    :param b: center diagonal vector from coefficient matrix
    :param c: east diagonal vector from coefficient matrix
    :param d: column vector
    :return: solution vector
    """

    n = len(d) - 1
    ac, bc, cc, dc = map(np.array, (a, b, c, d))  # copy arrays

    cc[0] /= bc[0]
    dc[0] /= bc[0]

    for i in range(1, n):
        cc[i] /= bc[i] - ac[i] * cc[i - 1]
        dc[i] = (dc[i] - ac[i] * dc[i - 1]) / (bc[i] - ac[i] * cc[i - 1])

    dc[n] = (dc[n] - ac[n] * dc[n - 1]) / (bc[n] - ac[n] * cc[n - 1])

    for i in reversed(range(0, n)):
        dc[i] -= cc[i] * dc[i + 1]

    return dc
