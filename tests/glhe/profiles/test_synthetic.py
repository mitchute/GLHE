import unittest

from glhe.profiles.synthetic import Synthetic


class TestSynthetic(unittest.TestCase):

    def test_get_value(self):
        tol = 1e-1
        tst = Synthetic('asymmetric', 1000)
        self.assertAlmostEqual(tst.get_value(0), -139.91, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), 0.3038, delta=tol)

        tst = Synthetic('symmetric', 1000)
        self.assertAlmostEqual(tst.get_value(0), -0.01, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), -0.01, delta=tol)
