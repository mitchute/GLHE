import unittest

from glhe.ground_temps.two_harmonic import TwoHarmonic


class TestTwoHarmonic(unittest.TestCase):

    def test_two_harmonic_ground_temp(self):
        tol = 1e-4
        tst = TwoHarmonic(15, 0, 0, 0, 0, 1e-6)
        self.assertAlmostEqual(tst.get_temp(0, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(15768000, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(15768000, 100), 15, delta=tol)

        tst = TwoHarmonic(15, 5, 0, 0, 0, 1e-6)
        self.assertAlmostEqual(tst.get_temp(0, 0), 10, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(15768000, 0), 20, delta=tol)
        self.assertAlmostEqual(tst.get_temp(15768000, 100), 15, delta=tol)
