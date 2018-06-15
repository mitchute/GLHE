import unittest

from glhe.groundTemps.single_harmonic import SingleHarmonic


class TestSingleHarmonic(unittest.TestCase):

    def test_single_harmonic_ground_temp(self):
        tol = 1e-4
        tst = SingleHarmonic(15, 0, 0, 1e-6)
        self.assertAlmostEqual(tst.get_temp(0, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(1555200, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(1555200, 100), 15, delta=tol)

        tst = SingleHarmonic(15, 5, 0, 1e-6)
        self.assertAlmostEqual(tst.get_temp(0, 0), 10, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(15768000, 0), 20, delta=tol)
        self.assertAlmostEqual(tst.get_temp(15768000, 100), 15, delta=tol)
