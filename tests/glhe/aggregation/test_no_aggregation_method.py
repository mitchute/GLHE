import unittest
from glhe.globals.variables import gv
from glhe.globals.functions import set_time_step

from glhe.aggregation.no_aggregation_method import NoAggMethod


class TestNoAgg(unittest.TestCase):

    def test_init(self):
        tst = NoAggMethod()
        self.assertEqual(len(tst.loads), 0)

    def test_add_load(self):
        gv.time_step = set_time_step(2)
        sim_time =0

        tst = NoAggMethod()

        sim_time += gv.time_step
        tst.add_load(gv.time_step, sim_time)
        tst.set_current_load(1)
        self.assertEqual(tst.loads[0].energy, 1)
