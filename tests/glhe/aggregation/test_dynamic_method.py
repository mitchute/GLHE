import unittest

from glhe.aggregation.dynamic_method import DynamicMethod


class TestDynamic(unittest.TestCase):

    def test_init(self):
        pass
        # tst = DynamicMethod()
        # self.assertEqual(len(tst.loads), 80)
        #
        # d = {'depth': 10, 'start width': 10, 'end width': 1}
        # tst = DynamicMethod(d)
        # self.assertEqual(len(tst.loads), 55)

    def test_add_load(self):
        pass
        # tst = DynamicMethod()
        # tst.add_load(1, 1)
        # tst.aggregate()
        # self.assertEqual(tst.loads[0].energy, 1)
        # tst.add_load(0, 1)
        # tst.aggregate()
        # self.assertEqual(tst.loads[0].energy, 0)
        # self.assertEqual(tst.loads[1].energy, 1)
