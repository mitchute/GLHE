import os
import tempfile
import unittest
from math import cos, sin

from numpy import arange, array
from numpy.linalg import solve as lin_alg_solve

from glhe.globals.functions import hanby
from glhe.globals.functions import load_json
from glhe.globals.functions import tdma_2
from glhe.globals.functions import runge_kutta_fourth_x
from glhe.globals.functions import set_time_step
from glhe.globals.functions import smoothing_function
from glhe.globals.functions import tdma_1
from glhe.globals.functions import temp_in_kelvin
from glhe.globals.functions import write_json


class TestFunctions(unittest.TestCase):

    def test_smoothing_function(self):
        tolerance = 0.001
        self.assertAlmostEqual(smoothing_function(x=-8, a=0, b=1), 0, delta=tolerance)
        self.assertAlmostEqual(smoothing_function(x=8, a=0, b=1), 1, delta=tolerance)

    def test_temp_in_kelvin(self):
        self.assertEqual(temp_in_kelvin(30), 303.15)

    def test_set_time_step(self):
        self.assertRaises(ZeroDivisionError, lambda: set_time_step(0))
        self.assertEqual(set_time_step(600), 60)
        self.assertEqual(set_time_step(60), 60)
        self.assertEqual(set_time_step(30), 120)
        self.assertEqual(set_time_step(15), 240)
        self.assertEqual(set_time_step(10), 360)
        self.assertEqual(set_time_step(1), 3600)

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

    def test_runge_kutta_fourth(self):
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
