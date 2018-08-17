import unittest

from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.globals.variables import gv


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = DynamicMethod()
        self.assertEqual(len(tst.loads), 5)

        d = {'depth': 10, 'start width': 10, 'end width': 1}
        tst = DynamicMethod(d)
        self.assertEqual(len(tst.loads), 5)

    def test_add_load(self):
        gv.time_step = 900
        tst = DynamicMethod()
        tst.add_load(1, 0)
        tst.update_aggregation(900)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(1800)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(2700)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(3600)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(4500)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(5400)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 2)

        tst.add_load(1, 0)
        tst.update_aggregation(6300)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.add_load(1, 0)
        tst.update_aggregation(7200)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)

        tst.add_load(1, 0)
        tst.update_aggregation(8100)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)
        self.assertEqual(tst.loads[6].energy, 1)

        tst.add_load(1, 0)
        tst.update_aggregation(9000)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)
        self.assertEqual(tst.loads[6].energy, 2)
