import unittest

from glhe.borehole.simpleHX import BoreholeSimpleHX


class TestBoreholeSimpleHX(unittest.TestCase):

    def test_get_outlet_temps(self):
        tst = BoreholeSimpleHX(None)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 25, 3)
        self.assertAlmostEqual(t2, 25, 3)

        t1, t2 = tst.get_outlet_temps(20, 20, 1)
        self.assertAlmostEqual(t1, 20, 3)
        self.assertAlmostEqual(t2, 20, 3)

        tst = BoreholeSimpleHX(None, effectiveness=1)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 30, 3)
        self.assertAlmostEqual(t2, 20, 3)

        tst = BoreholeSimpleHX(None, effectiveness=0)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 20, 3)
        self.assertAlmostEqual(t2, 30, 3)
