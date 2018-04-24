import unittest

from loads.bins.static_method import StaticMethod


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = StaticMethod(bin_nums=[1], bin_widths=[1])
        self.assertEqual(len(tst.loads), 0)
