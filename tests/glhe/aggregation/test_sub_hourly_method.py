import unittest

from glhe.aggregation.sub_hourly_method import SubHourMethod


class TestSubHourMethod(unittest.TestCase):

    def test_method(self):
        tst = SubHourMethod()

        tst.aggregate(900, 900, 1)
        pass
