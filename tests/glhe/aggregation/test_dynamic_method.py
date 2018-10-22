import unittest

from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.globals.variables import gv


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = DynamicMethod()
        self.assertEqual(len(tst.loads), 59)

        d = {'depth': 10, 'start width': 10, 'end width': 1}
        tst = DynamicMethod(d)
        self.assertEqual(len(tst.loads), 59)

    def test_add_load(self):
        gv.time_step = 900

        tst = DynamicMethod()

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1.75)
        self.assertEqual(tst.loads[5].energy, 0.25)
        self.assertEqual(tst.loads[6].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 2.3125)
        self.assertEqual(tst.loads[5].energy, 0.625)
        self.assertEqual(tst.loads[6].energy, 0.0625)
        self.assertEqual(tst.loads[7].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 2.734375)
        self.assertEqual(tst.loads[5].energy, 1.046875)
        self.assertEqual(tst.loads[6].energy, 0.203125)
        self.assertEqual(tst.loads[7].energy, 0.015625)
        self.assertEqual(tst.loads[8].energy, 0.)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 3.05078125)
        self.assertEqual(tst.loads[5].energy, 1.46875)
        self.assertEqual(tst.loads[6].energy, 0.4140625)
        self.assertEqual(tst.loads[7].energy, 0.0625)
        self.assertEqual(tst.loads[8].energy, 0.00390625)
        self.assertEqual(tst.loads[9].energy, 0)
