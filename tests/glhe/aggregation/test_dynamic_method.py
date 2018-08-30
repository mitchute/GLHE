import unittest

from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.globals.variables import gv


class TestDynamic(unittest.TestCase):

    def test_init(self):
        tst = DynamicMethod()
        self.assertEqual(len(tst.loads), 84)

        d = {'depth': 10, 'start width': 10, 'end width': 1}
        tst = DynamicMethod(d)
        self.assertEqual(len(tst.loads), 59)

    def test_add_load(self):
        gv.time_step = 900

        sim_time = 0

        tst = DynamicMethod()
        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1.75)
        self.assertEqual(tst.loads[5].energy, 0.25)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 2.3125)
        self.assertEqual(tst.loads[5].energy, 0.625)
        self.assertEqual(tst.loads[6].energy, 0.0625)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 2.734375)
        self.assertEqual(tst.loads[5].energy, 1.046875)
        self.assertEqual(tst.loads[6].energy, 0.203125)
        self.assertEqual(tst.loads[7].energy, 0.015625)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 3.05078125)
        self.assertEqual(tst.loads[5].energy, 1.46875)
        self.assertEqual(tst.loads[6].energy, 0.4140625)
        self.assertEqual(tst.loads[7].energy, 0.0625)
        self.assertEqual(tst.loads[8].energy, 0.00390625)

        tst.set_current_load(1)
        sim_time += gv.time_step
        tst.aggregate(sim_time)
        self.assertEqual(tst.loads[0].energy, 0)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 3.2880859375)
        self.assertEqual(tst.loads[5].energy, 1.8642578125)
        self.assertEqual(tst.loads[6].energy, 0.677734375)
        self.assertEqual(tst.loads[7].energy, 0.150390625)
        self.assertEqual(tst.loads[8].energy, 0.0185546875)
        self.assertEqual(tst.loads[9].energy, 0.0009765625)

