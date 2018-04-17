import unittest
from math import pi


from loads.loadProfile.sinusoid import Sinusoid


class TestSinusoid(unittest.TestCase):

    def test_get_load(self):
        tol = 1e-10

        tst = Sinusoid(1, 0, 2 * pi)
        self.assertAlmostEqual(tst.get_load(0), 0, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi / 2), 1, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi), 0, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi * 3 / 2), -1, delta=tol)
        self.assertAlmostEqual(tst.get_load(2 * pi), 0, delta=tol)

        tst = Sinusoid(1, 1, 2 * pi)
        self.assertAlmostEqual(tst.get_load(0), 1, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi / 2), 2, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi), 1, delta=tol)
        self.assertAlmostEqual(tst.get_load(pi * 3 / 2), 0, delta=tol)
        self.assertAlmostEqual(tst.get_load(2 * pi), 1, delta=tol)
