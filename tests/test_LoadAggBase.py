import unittest

from glhe.LoadAggregation import LoadAggBase


class TestLoadAggregation(unittest.TestCase):

    def test_a(self):
        tst = LoadAggBase()
        self.assertEqual(tst.loaded, True)
