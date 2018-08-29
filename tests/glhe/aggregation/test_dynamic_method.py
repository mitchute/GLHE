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
        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 2)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)
        self.assertEqual(tst.loads[6].energy, 1)

        tst.set_current_load(1, 0)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 4)
        self.assertEqual(tst.loads[6].energy, 2)
