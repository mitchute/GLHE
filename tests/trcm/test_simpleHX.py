import unittest

from glhe.trcm.simpleHX import TRCMSimpleHX


class TestTRCMCounterFlowHX(unittest.TestCase):

    def test_a(self):
        tst = TRCMSimpleHX(None)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 25, 3)
        self.assertAlmostEqual(t2, 25, 3)

        t1, t2 = tst.get_outlet_temps(20, 20, 1)
        self.assertAlmostEqual(t1, 20, 3)
        self.assertAlmostEqual(t2, 20, 3)

        tst = TRCMSimpleHX(None, effectiveness=1)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 30, 3)
        self.assertAlmostEqual(t2, 20, 3)

        tst = TRCMSimpleHX(None, effectiveness=0)
        t1, t2 = tst.get_outlet_temps(20, 30, 1)
        self.assertAlmostEqual(t1, 20, 3)
        self.assertAlmostEqual(t2, 30, 3)
