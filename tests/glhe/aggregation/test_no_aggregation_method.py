import unittest

from glhe.aggregation.no_aggregation_method import NoAggMethod
from glhe.globals.functions import num_ts_per_hour_to_sec_per_ts
from glhe.globals.variables import gv


class TestNoAgg(unittest.TestCase):

    def test_init(self):
        tst = NoAggMethod()
        self.assertEqual(len(tst.loads), 0)

    def test_add_load(self):
        gv.time_step = num_ts_per_hour_to_sec_per_ts(2)

        tst = NoAggMethod()

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
