import unittest

from glhe.profiles.synthetic_load import SyntheticLoad


class TestSynthetic(unittest.TestCase):

    def test_get_value(self):
        tol = 1e-1
        tst = SyntheticLoad('asymmetric', 1000)
        self.assertAlmostEqual(tst.get_value(0), -139.91, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), 0.3038, delta=tol)

        tst = SyntheticLoad('symmetric', 1000)
        self.assertAlmostEqual(tst.get_value(0), -0.01, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), -0.01, delta=tol)

        with self.assertRaises(Exception) as context:
            type = 'bob'
            SyntheticLoad(type, 1000)
        self.assertTrue("'{}' Synthetic object not supported. Check input.".format(type) in str(context.exception))
