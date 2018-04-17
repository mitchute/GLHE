import unittest


from loads.loadProfile.synthetic import Asymmetric, Symmetric


class TestAsymmetric(unittest.TestCase):

    def test_get_load(self):
        tol = 1e-1
        tst = Asymmetric(1000)
        self.assertAlmostEqual(tst.get_load(0), -139.91, delta=tol)
        self.assertAlmostEqual(tst.get_load(8760), -16.07, delta=tol)


class TestSymmetric(unittest.TestCase):

    def test_get_load(self):
        tol = 1e-1
        tst = Symmetric(1000)
        self.assertAlmostEqual(tst.get_load(0), -0.01, delta=tol)
        self.assertAlmostEqual(tst.get_load(8760), -119.04, delta=tol)
