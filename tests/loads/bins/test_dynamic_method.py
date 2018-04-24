import unittest

from loads.bins.dynamic_method import DynamicMethod


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = DynamicMethod()
        self.assertEqual(len(tst.loads), 80)

        tst = DynamicMethod(depth=10, start_width=10, end_width=1)
        self.assertEqual(len(tst.loads), 55)

    def test_add_load(self):
        tst = DynamicMethod()
        tst.add_load(1)
        self.assertEqual(tst.loads[0].energy, 1)
        tst.add_load(0)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
