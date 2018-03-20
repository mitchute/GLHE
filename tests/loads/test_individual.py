import unittest

from glhe.loads.individual import LoadAggregationIndividual


class TestLoadAggregation(unittest.TestCase):

    def test_a(self):
        tst = LoadAggregationIndividual()
        tst.store_load(1, 10)
        self.assertEqual(tst.get_load(10), 1)
