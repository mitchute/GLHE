import unittest

from glhe.aggregation.static_method import StaticMethod
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.functions import set_time_step
from glhe.globals.variables import gv


class TestStatic(unittest.TestCase):

    def test_init(self):
        tst = StaticMethod()
        self.assertEqual(len(tst.loads), 0)

    def test_add_load(self):
        d = {'min number bins': [2, 2, 2], 'bin widths in hours': [1, 2, 4], 'min sub-hour bins': 2}
        gv.time_step = set_time_step(2)
        tst = StaticMethod(d)
        tst.set_current_load(1, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)

        tst.set_current_load(2, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 2)
        self.assertEqual(tst.loads[1].energy, 1)

        tst.set_current_load(3, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 3)
        self.assertEqual(tst.loads[1].energy, 2)
        self.assertEqual(tst.loads[2].energy, 1)

        tst.set_current_load(4, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 4)
        self.assertEqual(tst.loads[1].energy, 3)
        self.assertEqual(tst.loads[2].energy, 3)

        tst.set_current_load(5, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 5)
        self.assertEqual(tst.loads[1].energy, 4)
        self.assertEqual(tst.loads[2].energy, 3)
        self.assertEqual(tst.loads[3].energy, 3)

        tst.set_current_load(6, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 6)
        self.assertEqual(tst.loads[1].energy, 5)
        self.assertEqual(tst.loads[2].energy, 7)
        self.assertEqual(tst.loads[3].energy, 3)

        tst.set_current_load(7, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 7)
        self.assertEqual(tst.loads[1].energy, 6)
        self.assertEqual(tst.loads[2].energy, 5)
        self.assertEqual(tst.loads[3].energy, 7)
        self.assertEqual(tst.loads[4].energy, 3)

        tst.set_current_load(8, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 8)
        self.assertEqual(tst.loads[1].energy, 7)
        self.assertEqual(tst.loads[2].energy, 11)
        self.assertEqual(tst.loads[3].energy, 7)
        self.assertEqual(tst.loads[4].energy, 3)

        tst.set_current_load(9, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 9)
        self.assertEqual(tst.loads[1].energy, 8)
        self.assertEqual(tst.loads[2].energy, 7)
        self.assertEqual(tst.loads[3].energy, 11)
        self.assertEqual(tst.loads[4].energy, 7)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.set_current_load(10, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 10)
        self.assertEqual(tst.loads[1].energy, 9)
        self.assertEqual(tst.loads[2].energy, 15)
        self.assertEqual(tst.loads[3].energy, 11)
        self.assertEqual(tst.loads[4].energy, 7)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.set_current_load(11, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 11)
        self.assertEqual(tst.loads[1].energy, 10)
        self.assertEqual(tst.loads[2].energy, 9)
        self.assertEqual(tst.loads[3].energy, 15)
        self.assertEqual(tst.loads[4].energy, 11)
        self.assertEqual(tst.loads[5].energy, 10)

        tst.set_current_load(12, SEC_IN_HOUR)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 12)
        self.assertEqual(tst.loads[1].energy, 11)
        self.assertEqual(tst.loads[2].energy, 19)
        self.assertEqual(tst.loads[3].energy, 15)
        self.assertEqual(tst.loads[4].energy, 11)
        self.assertEqual(tst.loads[5].energy, 10)

    def test_add_load_with_sub_hour_loads(self):
        d = {'min number bins': [2, 2, 2], 'bin widths in hours': [1, 2, 4], 'min sub-hour bins': 2}
        gv.time_step = set_time_step(2)
        tst = StaticMethod(d)
        tst.set_current_load(0.5, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 0.5)  # width: 1800

        tst.set_current_load(1, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1.0)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 0.5)  # width: 1800

        tst.set_current_load(1.5, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1.5)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 1.0)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 0.5)  # width: 1800

        tst.set_current_load(2.0, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 2.0)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 1.5)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 1.5)  # width: 3600

        tst.set_current_load(2.5, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 2.5)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 2.0)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 1.5)  # width: 1800
        self.assertEqual(tst.loads[3].energy, 1.5)  # width: 3600

        tst.set_current_load(3.0, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 3.0)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 2.5)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 3.5)  # width: 3600
        self.assertEqual(tst.loads[3].energy, 1.5)  # width: 3600

        tst.set_current_load(3.5, SEC_IN_HOUR / 2)
        self.assertEqual(tst.loads[0].energy, 3.5)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 3.0)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 2.5)  # width: 1800
        self.assertEqual(tst.loads[3].energy, 3.5)  # width: 3600
        self.assertEqual(tst.loads[4].energy, 1.5)  # width: 3600

        tst.set_current_load(4.0, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 4.0)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 3.5)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 5.5)  # width: 3600
        self.assertEqual(tst.loads[3].energy, 3.5)  # width: 3600
        self.assertEqual(tst.loads[4].energy, 1.5)  # width: 3600

        tst.set_current_load(4.5, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 4.5)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 4.0)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 3.5)  # width: 1800
        self.assertEqual(tst.loads[3].energy, 5.5)  # width: 3600
        self.assertEqual(tst.loads[4].energy, 3.5)  # width: 3600
        self.assertEqual(tst.loads[5].energy, 1.5)  # width: 3600

        tst.set_current_load(5.0, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 5.0)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 4.5)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 7.5)  # width: 3600
        self.assertEqual(tst.loads[3].energy, 5.5)  # width: 3600
        self.assertEqual(tst.loads[4].energy, 3.5)  # width: 3600
        self.assertEqual(tst.loads[5].energy, 1.5)  # width: 3600

        tst.set_current_load(5.5, SEC_IN_HOUR / 2)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 5.5)  # width: 1800
        self.assertEqual(tst.loads[1].energy, 5.0)  # width: 1800
        self.assertEqual(tst.loads[2].energy, 4.5)  # width: 1800
        self.assertEqual(tst.loads[3].energy, 7.5)  # width: 3600
        self.assertEqual(tst.loads[4].energy, 5.5)  # width: 3600
        self.assertEqual(tst.loads[5].energy, 5.0)  # width: 3600
