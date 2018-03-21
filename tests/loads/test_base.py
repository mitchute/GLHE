import unittest

from glhe.loads.base import LoadAggregationBase


class TestLoadAggregationBase(unittest.TestCase):

    def test_a(self):
        tst = LoadAggregationBase()
        self.assertEquals(tst.get_load(1), None)
        self.assertEquals(tst.store_load(1, 1), None)
