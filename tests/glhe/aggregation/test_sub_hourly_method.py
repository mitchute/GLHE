import unittest

from glhe.aggregation.sub_hourly_method import SubHourMethod


class TestSubHourMethod(unittest.TestCase):

    def test_method(self):
        tst = SubHourMethod()

        # assuming t = 0 has already happened
        dt_sml = 900
        dt_med = 1800
        dt_lrg = 3150
        dt_huge = 3600

        # no shift
        t = 900
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # full bin shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 1)

        # full bin shift x 2
        t += dt_med
        val = tst.aggregate(t, 2)
        self.assertEqual(val, 2)

        # full bin shift x 4
        t += dt_huge
        val = tst.aggregate(t, 4)
        self.assertEqual(val, 4)

        # partial bin shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 1)

        # full and partial bin shift
        t += dt_lrg
        val = tst.aggregate(t, 3.5)
        self.assertEqual(val, 3.5)
