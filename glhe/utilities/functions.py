import csv
import json
from abc import ABC, abstractmethod
from math import ceil, exp, factorial, floor
from pathlib import Path
from typing import Callable, overload

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d

from glhe.utilities.constants import SEC_IN_HOUR


def smoothing_function(x: float, a: float, b: float) -> float:
    """
    Sigmoid smoothing function

    https://en.wikipedia.org/wiki/Sigmoid_function

    :param x: independent variable
    :param a: fitting parameter 1
    :param b: fitting parameter 2
    :return: float between 0-1
    """

    return 1 / (1 + exp(-(x - a) / b))


@overload
def k_to_c(x: int) -> int:
    pass


@overload
def k_to_c(x: float) -> float:
    pass


@overload
def k_to_c(x: np.ndarray) -> np.ndarray:
    pass


def k_to_c(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts Kelvin to Celsius

    :param x: temperature in Kelvin
    :return: temperature in Celsius
    """

    return x - 273.15


@overload
def c_to_k(x: int) -> int:
    pass


@overload
def c_to_k(x: float) -> float:
    pass


@overload
def c_to_k(x: np.ndarray) -> np.ndarray:
    pass


def c_to_k(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts Celsius to Kelvin

    :param x: temperature in Celsius
    :return: temperature in Kelvin
    """

    return x + 273.15


@overload
def sec_to_hr(x: int) -> int:
    pass


@overload
def sec_to_hr(x: float) -> float:
    pass


@overload
def sec_to_hr(x: np.ndarray) -> np.ndarray:
    pass


def sec_to_hr(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts seconds to hours

    :param x: input in seconds
    :return: output in hours
    """

    return x / SEC_IN_HOUR


@overload
def hr_to_sec(x: int) -> int:
    pass


@overload
def hr_to_sec(x: float) -> float:
    pass


@overload
def hr_to_sec(x: np.ndarray) -> np.ndarray:
    pass


def hr_to_sec(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts hours to seconds

    :param x: input in hours
    :return: output in seconds
    """

    return x * SEC_IN_HOUR


@overload
def kw_to_w(x: int) -> int:
    pass


@overload
def kw_to_w(x: float) -> float:
    pass


@overload
def kw_to_w(x: np.ndarray) -> np.ndarray:
    pass


def kw_to_w(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts kW to W

    :param x: input in kW
    :return: output in W
    """

    return x * 1000


@overload
def w_to_kw(x: int) -> int:
    pass


@overload
def w_to_kw(x: float) -> float:
    pass


@overload
def w_to_kw(x: np.ndarray) -> np.ndarray:
    pass


def w_to_kw(x: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Converts W to kW

    :param x: input in W
    :return: output in kW
    """

    return x / 1000


def num_ts_per_hour_to_sec_per_ts(time_step_per_hour: int) -> int:
    """
    Converts the input time-steps per hour to the nearest possible time-step in seconds.
    Time-step should be evenly divisible into an hour.

    :param time_step_per_hour: number of simulation time steps per hour
    :return: time step in seconds
    """
    try:
        input_time_step = int(SEC_IN_HOUR / time_step_per_hour)
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


def load_json(input_path: str) -> dict:
    """
    Loads a json file

    :param input_path: file path
    :return: loaded json object as parsed dict object
    """

    with open(input_path, 'r') as f:
        json_blob = f.read()
    return json.loads(json_blob)


def write_json(write_path: Path, input_dict: dict, indent: int = 2) -> None:
    with write_path.open('w') as f:
        f.write(json.dumps(input_dict, sort_keys=True, indent=indent, separators=(',', ': ')))


def hanby(time: float, vol_flow_rate: float, volume: float) -> float:
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


def merge_dicts(d_root: dict, d_append: dict) -> dict:
    """
    Return new dictionary with d_append added to d_root at the root level

    :param d_root: input dictionary
    :param d_append: the dictionary to append
    :return: combined dict
    """

    return {**d_root, **d_append}


def runge_kutta_fourth_xy(rhs: Callable[[float, float], float], h: float, x: float, y: float) -> float:
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects both x and y variables.

    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.

    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g. dy/dx = f(x, y))
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


def runge_kutta_fourth_x(rhs: Callable[[float], float], h: float, x: float, y: float) -> float:
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects only the x variable.

    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.

    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g. dy/dx = f(x))
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


def runge_kutta_fourth_y(rhs: Callable[[float], float], h: float, y: float) -> float:
    """
    Solves one step using a fourth-order Runge-Kutta method. RHS expects only the y variable.
    Moin, P. 2010. Fundamentals of Engineering Numerical Analysis. 2nd ed.
    Cambridge University Press. New York, New York.
    :param rhs: "Right-hand Side" of the equation(s). Everything but the derivative. (e.g. dy/dx = f(y))
    :param h: step size
    :param y: output dimension
    :return:
    """

    k_1 = rhs(y)
    k_2 = rhs(y + k_1 / 2.0)
    k_3 = rhs(y + k_2 / 2.0)
    k_4 = rhs(y + k_3)

    return y + (k_1 + 2 * (k_2 + k_3) + k_4) / 6.0 * h


def tdma_1(a: list | np.ndarray, b: list | np.ndarray, c: list | np.ndarray, d: list | np.ndarray) -> np.ndarray:
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
    :return: solution vector
    """

    n = len(d)  # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d))  # copy arrays

    for i in range(1, n):
        mc = ac[i - 1] / bc[i - 1]
        bc[i] = bc[i] - mc * cc[i - 1]
        dc[i] = dc[i] - mc * dc[i - 1]

    xc = bc
    xc[-1] = dc[-1] / bc[-1]

    for i in range(n - 2, -1, -1):
        xc[i] = (dc[i] - cc[i] * xc[i + 1]) / bc[i]

    return xc


def tdma_2(a: list | np.ndarray, b: list | np.ndarray, c: list | np.ndarray, d: list | np.ndarray) -> np.ndarray:
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
    ac, bc, cc, dc = (x.astype(float) for x in (a, b, c, d))  # copy arrays

    cc[0] /= bc[0]
    dc[0] /= bc[0]

    for i in range(1, n):
        cc[i] /= bc[i] - ac[i] * cc[i - 1]
        dc[i] = (dc[i] - ac[i] * dc[i - 1]) / (bc[i] - ac[i] * cc[i - 1])

    dc[n] = (dc[n] - ac[n] * dc[n - 1]) / (bc[n] - ac[n] * cc[n - 1])

    for i in reversed(range(0, n)):
        dc[i] -= cc[i] * dc[i + 1]

    return dc


@overload
def lower_obj(x: list) -> list:
    pass


@overload
def lower_obj(x: dict) -> dict:
    pass


@overload
def lower_obj(x: str) -> str:
    pass


def lower_obj(x: list | dict | str) -> list | dict | str:
    """
    Lower cases objects, including nested objects.

    Adapted from here: https://stackoverflow.com/a/4223871/5965685

    :param x: input object
    :return: output object lower-cased
    """

    ignored_fields = ['path', 'g-function-path', 'g_b-function-path']

    if isinstance(x, list):
        return [lower_obj(v) for v in x]
    elif isinstance(x, dict):
        d = {}
        for k, v in x.items():
            if k.lower() in ignored_fields:
                d[k.lower()] = v
            else:
                d[k.lower()] = lower_obj(v)
        return d
    elif isinstance(x, str):
        return x.lower()
    else:  # TODO: Probably should complain about the unknown type?
        return x


def lin_interp(x: float, x_l: float, x_h: float, y_l: float, y_h: float) -> float:
    """
    Simple linear interpolation.

    :param x: independent input variable
    :param x_l: low independent interval bound
    :param x_h: high independent interval bound
    :param y_l: low dependent interval bound
    :param y_h: high dependent interval bound
    :return: interpolated value
    """

    return (x - x_l) / (x_h - x_l) * (y_h - y_l) + y_l


def un_reverse_idx(length: int, reversed_idx: int) -> int:
    """
    For a reversed list-like object, this will return the index for the entry within the original un-reversed list

    :param length: length of list-like object
    :param reversed_idx: index of item in reversed list
    :return: index of the same object in the un-reversed list
    """

    return length - 1 - reversed_idx


def write_arrays_to_csv(path: Path, arrays: list | np.ndarray) -> None:
    _arrays = None
    if isinstance(arrays, list):
        _arrays = np.array(arrays)
    else:
        _arrays = arrays
    data = _arrays.T
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


class InterpolatorBase(ABC):
    @abstractmethod
    def interpolate(self, *args: list[float]) -> float:
        pass


class Interpolator1D(InterpolatorBase):

    def __init__(self, x_data: np.ndarray, y_data: np.ndarray | list[float]):
        """
        1D Interpolation Class, currently a wrapper for scipy interpolator, but soon just a simple interpolator

        :param x_data: Numpy array of x-value floats
        :param y_data: Numpy array of x-value floats
        """
        self.interp = interp1d(x_data, y_data, fill_value='extrapolate')

    def interpolate(self, *args: list[float]) -> float:
        return self.interp(args[0])


class Interpolator1DFromFile(Interpolator1D):
    def __init__(self, data_path: Path):
        """
        1D Interpolation Class, currently a wrapper for scipy interpolator, but soon just a simple interpolator

        :param data_path: path to csv file with columned data, e.g. 'x1,y1'
        """
        data = np.genfromtxt(str(data_path), delimiter=',')
        _, num_col = data.shape
        if num_col != 2:
            raise ValueError("Number of columns in '{}' must be 2".format(data_path))
        super().__init__(data[:, 0], data[:, 1])


class Interpolator2DFromFile(InterpolatorBase):
    def __init__(self, xz_data_path: Path, y: list):
        """
        2D interpolation class, currently a wrapper for scipy interpolator, but soon just a simple interpolator

        Example data:
        x1, y1, z1, x2, y2, z2
        1,   3,  5,  1,  4,  6
        2,   3,  6,  2,  4,  7
        3,   3   7,  3,  4,  8

        xy_data_path will lead to a file such as:

        1,5,6\n
        2,6,7\n
        3,7,8\n

        y will be: [3, 4]

        :param xz_data_path: path to csv file with columned data, e.g. 'x1,z1,z2,...,zn'
        :param y: list of *constant* values for the second independent variable
        """

        data = np.genfromtxt(str(xz_data_path), delimiter=',')
        _, num_col = data.shape

        num_series = num_col - 1

        # check to make sure number of columns and length of 'y' match
        if num_series != len(y):
            ValueError("Number of columns in '{}' inconsistent with 'y'".format(xz_data_path))

        x = data[:, 0]
        z = np.ndarray(shape=(len(x), num_series))
        for idx in range(num_series):
            z[:, idx] = data[:, idx + 1]

        self.interp = RegularGridInterpolator((x, y), z)

    def interpolate(self, *args: list[float]) -> float:
        x = self.interp(args)
        return x.min()  # just want to get the first item, this works fine, but could do better


def resample_g_functions(lntts, g, lntts_interval=0.1):
    """
    Resample g-function data at regular ln(t/ts) intervals

    :param lntts: input ln(t/ts) data
    :param g: corresponding g-function data
    :param lntts_interval: resample interval
    """

    # make sure lntts and g have the same number of elements
    if len(lntts) != len(g):
        raise ValueError('Number of lntts and g elements is not consistent')

    # min/max lntts values
    min_lntts = lntts_interval * ceil(lntts[0] / lntts_interval)
    max_lntts = lntts_interval * floor(lntts[-1] / lntts_interval)

    new_lntts = np.arange(min_lntts, max_lntts + lntts_interval, lntts_interval)

    f = interp1d(lntts, g)
    new_g = f(new_lntts)

    return new_lntts, new_g
