import unittest

from glhe.aggregation.sub_hourly_method import SubHourMethod


class TestSubHourMethod(unittest.TestCase):

    def test_method(self):
        tst = SubHourMethod()

        # assuming t = 0 has already happened
        t = 1200
        dt = 1200
        tst.aggregate(t, 1)
        t += dt
        tst.aggregate(t, 1)
        t += dt
        tst.aggregate(t, 1)
        t += dt
        tst.aggregate(t, 1)
        t += dt
        tst.aggregate(t, 1)
        t += dt
        tst.aggregate(t, 1)
