import os
import tempfile
import unittest

from math import cos, sin
from numpy import arange, array
from numpy.linalg import solve as lin_alg_solve
from scipy.interpolate.interpolate import interp1d
from scipy.interpolate.interpolate import interp2d

from glhe.utilities.functions import c_to_k
from glhe.utilities.functions import hanby
from glhe.utilities.functions import hr_to_sec
from glhe.utilities.functions import kw_to_w
from glhe.utilities.functions import lin_interp
from glhe.utilities.functions import load_interp1d
from glhe.utilities.functions import load_interp2d
from glhe.utilities.functions import load_json
from glhe.utilities.functions import lower_obj
from glhe.utilities.functions import merge_dicts
from glhe.utilities.functions import num_ts_per_hour_to_sec_per_ts
from glhe.utilities.functions import resample_g_functions
from glhe.utilities.functions import runge_kutta_fourth_x
from glhe.utilities.functions import runge_kutta_fourth_xy
from glhe.utilities.functions import runge_kutta_fourth_y
from glhe.utilities.functions import sec_to_hr
from glhe.utilities.functions import smoothing_function
from glhe.utilities.functions import tdma_1
from glhe.utilities.functions import tdma_2
from glhe.utilities.functions import write_arrays_to_csv
from glhe.utilities.functions import write_json


class TestFunctions(unittest.TestCase):

    def test_smoothing_function(self):
        tolerance = 0.001
        self.assertAlmostEqual(smoothing_function(x=-8, a=0, b=1), 0, delta=tolerance)
        self.assertAlmostEqual(smoothing_function(x=8, a=0, b=1), 1, delta=tolerance)

    def test_temp_in_kelvin(self):
        self.assertEqual(c_to_k(30), 303.15)

    def test_kw_to_w(self):
        self.assertEqual(kw_to_w(1), 1000)

    def test_set_time_step(self):
        self.assertRaises(ZeroDivisionError, lambda: num_ts_per_hour_to_sec_per_ts(0))
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(600), 60)
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(60), 60)
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(30), 120)
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(15), 240)
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(10), 360)
        self.assertEqual(num_ts_per_hour_to_sec_per_ts(1), 3600)

    def test_load_json(self):
        temp_directory = tempfile.mkdtemp()
        temp_json_file = os.path.join(temp_directory, 'temp.json')
        with open(temp_json_file, 'w') as f:
            f.write('{"key": "value", "key 2": 1}')

        d = load_json(temp_json_file)

        self.assertEqual(d["key"], "value")
        self.assertEqual(d["key 2"], 1)

    def test_write_json(self):
        temp_directory = tempfile.mkdtemp()
        temp_file = os.path.join(temp_directory, 'temp.json')

        d = {
            "key": "value",
            "key 2": 2
        }

        write_json(temp_file, d)
        loaded = load_json(temp_file)
        self.assertEqual(d, loaded)

    def test_hanby(self):
        tolerance = 0.00001
        self.assertAlmostEqual(hanby(0.0, 1, 1), 0, delta=tolerance)
        self.assertAlmostEqual(hanby(0.3, 1, 1), 0, delta=tolerance)
        self.assertAlmostEqual(hanby(0.5, 1, 1), 1.5e-5, delta=tolerance)
        self.assertAlmostEqual(hanby(0.8, 1, 1), 0.07939, delta=tolerance)
        self.assertAlmostEqual(hanby(1.0, 1, 1), 0.5196, delta=tolerance)
        self.assertAlmostEqual(hanby(1.5, 1, 1), 0.99863, delta=tolerance)

    def test_runge_kutta_fourth_x(self):
        tol = 1E-4
        omega = 4

        def f(x):
            return cos(omega * x)

        def f_prime(x):
            return -omega * sin(omega * x)

        start = 0
        stop = 6
        step = 0.15

        x_arr = arange(start=start, stop=stop, step=step)
        y = array([1])

        for x in x_arr:
            y = runge_kutta_fourth_x(f_prime, step, x=x, y=y)
            y_act = f(x + step)

            self.assertAlmostEqual(y_act, y, delta=tol)

    def test_runge_kutta_fourth_xy(self):

        # Derivative
        # dy/dx = x ** 2 / (1 - y **2)

        # General solution
        # (-x ** 3 / 3) + y (y ** 3 / 3) = C

        def f_prime(x, y):
            return x ** 2 / (1 - y ** 2)

        y = runge_kutta_fourth_xy(f_prime, 0, x=2, y=2)
        y_act = 2

        self.assertAlmostEqual(y_act, y, delta=0.001)

    def test_runge_kutta_fourth_y(self):

        # Derivative
        # dy/dt = y * (1 - y)

        # Solution
        # y(t) = 1 / (1 + exp(-t))

        def f_prime(x):
            return x * (1 - x)

        y = runge_kutta_fourth_y(f_prime, 0, y=0.5)
        y_act = 0.5

        self.assertAlmostEqual(y_act, y, delta=0.001)

    def test_tdma_1(self):

        tol = 0.000001

        A = array([[10, 2, 0, 0], [3, 10, 4, 0], [0, 1, 7, 5], [0, 0, 3, 4]], dtype=float)

        a = array([3, 1, 3], dtype=float)
        b = array([10, 10, 7, 4], dtype=float)
        c = array([2, 4, 5], dtype=float)
        d = array([3, 4, 5, 6], dtype=float)

        tst = tdma_1(a, b, c, d)

        soln = lin_alg_solve(A, d)

        for idx, _ in enumerate(tst):
            self.assertAlmostEqual(tst[idx], soln[idx], delta=tol)

    def test_tdma_2(self):

        tol = 0.000001

        A = array([[10, 2, 0, 0], [3, 10, 4, 0], [0, 1, 7, 5], [0, 0, 3, 4]], dtype=float)

        a = array([0, 3, 1, 3], dtype=float)
        b = array([10, 10, 7, 4], dtype=float)
        c = array([2, 4, 5, 0], dtype=float)
        d = array([3, 4, 5, 6], dtype=float)

        tst = tdma_2(a, b, c, d)

        soln = lin_alg_solve(A, d)

        for idx, _ in enumerate(tst):
            self.assertAlmostEqual(tst[idx], soln[idx], delta=tol)

    def test_merge_dict(self):
        d_merged = merge_dicts({'key 1': 1}, {'key 2': 2})
        self.assertTrue('key 1' in d_merged.keys())
        self.assertTrue('key 2' in d_merged.keys())

        self.assertEqual(d_merged['key 1'], 1)
        self.assertEqual(d_merged['key 2'], 2)

    def test_lower_obj(self):

        d = {'Outer Key 1': 'VAL',
             'Outer Key 2': 2,
             'Nested Obj': {'Inner Key 1': [1, 2.3, 5],
                            'Inner Key 2': 2.635,
                            'Inner Key 3': ['Red', 'tEd', 2.3]},
             'Path': '/this/is/SOME/Path',
             'NAME': 'My Name'}

        ret = lower_obj(d)

        self.assertEqual(d['Outer Key 1'].lower(), ret['outer key 1'])
        self.assertEqual(d['Outer Key 2'], ret['outer key 2'])
        self.assertEqual(d['Nested Obj']['Inner Key 1'], ret['nested obj']['inner key 1'])
        self.assertEqual(d['Nested Obj']['Inner Key 2'], ret['nested obj']['inner key 2'])
        self.assertEqual(d['Nested Obj']['Inner Key 3'][0].lower(), ret['nested obj']['inner key 3'][0])
        self.assertEqual(d['Nested Obj']['Inner Key 3'][1].lower(), ret['nested obj']['inner key 3'][1])
        self.assertEqual(d['Nested Obj']['Inner Key 3'][2], ret['nested obj']['inner key 3'][2])
        self.assertEqual(d['Path'], ret['path'])

    def test_hr_to_sec(self):
        self.assertEqual(hr_to_sec(1), 3600)

    def test_sec_to_hr(self):
        self.assertEqual(sec_to_hr(3600), 1)

    def test_lin_interp(self):
        self.assertEqual(lin_interp(0, 0, 2, 0, 2), 0)
        self.assertEqual(lin_interp(1, 0, 2, 0, 2), 1)
        self.assertEqual(lin_interp(2, 0, 2, 0, 2), 2)

    def test_write_arrays_to_csv(self):
        temp_dir = tempfile.mkdtemp()
        file_name = 'out.csv'
        path = os.path.join(temp_dir, file_name)
        a_1 = [1, 2, 3]
        a_2 = [4, 5, 6]
        write_arrays_to_csv(path, [a_1, a_2])

        with open(path, 'r') as f:
            for idx, line in enumerate(f):
                tokens = line.split(',')
                self.assertEqual(float(tokens[0]), a_1[idx])
                self.assertEqual(float(tokens[1]), a_2[idx])

        a_1 = array([1, 2, 3])
        a_2 = array([4, 5, 6])
        a_3 = array([a_1, a_2])

        write_arrays_to_csv(path, a_3)

        with open(path, 'r') as f:
            for idx, line in enumerate(f):
                tokens = line.split(',')
                self.assertEqual(float(tokens[0]), a_1[idx])
                self.assertEqual(float(tokens[1]), a_2[idx])

    def test_resample_g_functions(self):

        lntts = [-16.5, -16.0, -15.5, -15.5, -15.0, -14.5, -14.0]
        g = [0, 1, 2, 3, 4, 5, 6]

        new_lntts, new_g = resample_g_functions(lntts, g, lntts_interval=0.25)

        self.assertEqual(new_lntts[0], -16.50)
        self.assertEqual(new_lntts[1], -16.25)
        self.assertEqual(new_lntts[-2], -14.25)
        self.assertEqual(new_lntts[-1], -14.00)


class TestInterp1D(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        f_path = os.path.join(temp_dir, 'temp.csv')
        with open(f_path, 'w') as f:
            f.write('0,5\n')
            f.write('1,6\n')
            f.write('2,7\n')

        return load_interp1d(f_path)

    def test_init(self):
        tst = self.add_instance()
        self.assertTrue(isinstance(tst, interp1d))

    def test_get_value(self):
        tst = self.add_instance()

        self.assertEqual(tst(0), 5)
        self.assertEqual(tst(1), 6)
        self.assertEqual(tst(2), 7)


class TestInterp2D(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        f_path = os.path.join(temp_dir, 'temp.csv')
        with open(f_path, 'w') as f:
            f.write('0,5,8\n')
            f.write('1,6,9\n')
            f.write('2,7,10\n')

        return load_interp2d(f_path, [3, 4])

    def test_init(self):
        tst = self.add_instance()
        self.assertTrue(isinstance(tst, interp2d))

    def test_get_value(self):
        tst = self.add_instance()

        self.assertEqual(tst(0, 3), 5)
        self.assertEqual(tst(1, 3), 6)
        self.assertEqual(tst(2, 3), 7)

        self.assertEqual(tst(0, 4), 8)
        self.assertEqual(tst(1, 4), 9)
        self.assertEqual(tst(2, 4), 10)

        self.assertEqual(tst(0.5, 3.5), 7)
        self.assertEqual(tst(1.5, 3.5), 8)
