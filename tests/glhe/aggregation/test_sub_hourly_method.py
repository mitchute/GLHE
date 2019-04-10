import os
import tempfile
import unittest

from glhe.aggregation.sub_hourly import SubHour


class TestSubHourMethod(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        temp_csv = os.path.join(temp_dir, 'temp.csv')

        with open(temp_csv, 'w') as f:
            f.write('-14, 0\n-13, 1\n-12, 2\n')

        d = {'method': 'dynamic',
             'expansion-rate': 2,
             'number-bins-per-level': 2,
             'runtime': 36000,
             'time-scale': 5e9,
             'g-function-path': temp_csv}

        return SubHour(d)

    def test_aggregate(self):
        tst = self.add_instance()

        # assuming t = 0 has already happened
        dt_huge = 3600
        dt_lrg = 3150
        dt_med = 1800
        dt_sml = 900

        # no shift
        t = 900
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # no shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 0)

        # full bin shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 1)

        # full bin shift x 2
        t += dt_med
        val = tst.aggregate(t, 2)
        self.assertEqual(val, 2)

        # full bin shift x 4
        t += dt_huge
        val = tst.aggregate(t, 4)
        self.assertEqual(val, 4)

        # partial bin shift
        t += dt_sml
        val = tst.aggregate(t, 1)
        self.assertEqual(val, 1)

        # full and partial bin shift
        t += dt_lrg
        val = tst.aggregate(t, 3.5)
        self.assertEqual(val, 3.5)
