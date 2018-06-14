import unittest
from math import pi

from loads.profiles.sinusoid import Sinusoid


class TestSinusoid(unittest.TestCase):

    def test_get_load(self):
        tol = 1e-10

        tst = Sinusoid(1, 0, 2 * pi)
        self.assertAlmostEqual(tst.get_value(0), 0, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi / 2), 1, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi), 0, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi * 3 / 2), -1, delta=tol)
        self.assertAlmostEqual(tst.get_value(2 * pi), 0, delta=tol)

        tst = Sinusoid(1, 1, 2 * pi)
        self.assertAlmostEqual(tst.get_value(0), 1, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi / 2), 2, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi), 1, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi * 3 / 2), 0, delta=tol)
        self.assertAlmostEqual(tst.get_value(2 * pi), 1, delta=tol)
