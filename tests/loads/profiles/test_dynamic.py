import unittest

from loads.bins.dynamic import DynamicBin


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = DynamicBin()
        self.assertEqual(len(tst.loads), 80)
