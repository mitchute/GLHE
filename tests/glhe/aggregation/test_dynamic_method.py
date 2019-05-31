import os
import tempfile
import unittest

import numpy as np

from glhe.aggregation.dynamic import Dynamic


class TestDynamic(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        temp_csv = os.path.join(temp_dir, 'temp.csv')

        with open(temp_csv, 'w') as f:
            f.write('-16, 0\n'
                    '-14, 1\n'
                    '-12, 2\n'
                    '-10, 3\n'
                    '-8, 4\n')

        d = {'method': 'dynamic',
             'expansion-rate': 2,
             'number-bins-per-level': 2,
             'runtime': 36000,
             'time-scale': 5e9,
             'g-function-path': temp_csv}

        return Dynamic(d)

    @staticmethod
    def add_instance_g_b():
        temp_dir = tempfile.mkdtemp()
        temp_csv = os.path.join(temp_dir, 'temp.csv')
        temp_csv_2 = os.path.join(temp_dir, 'temp_2.csv')

        with open(temp_csv, 'w') as f:
            f.write('-16, 0\n'
                    '-14, 1\n'
                    '-12, 2\n'
                    '-10, 3\n'
                    '-8, 4\n')

        with open(temp_csv_2, 'w') as f:
            f.write('-16, 0\n'
                    '-14, 1\n'
                    '-12, 2\n'
                    '-10, 3\n'
                    '-8, 4\n')

        d = {'method': 'dynamic',
             'expansion-rate': 2,
             'number-bins-per-level': 2,
             'runtime': 36000,
             'time-scale': 5e9,
             'g-function-path': temp_csv,
             'g_b-function-path': temp_csv_2}

        return Dynamic(d)

    def test_aggregate(self):
        tst = self.add_instance()

        dt_lrg = 3600
        dt_med = 1800
        dt_sml = 900
        t = 0

        # hour 1
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.energy), 0)

        # hour 2
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.energy), 4)

        # hour 3
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.energy), 8)

        # hour 3.5
        t += dt_med
        tst.aggregate(t, 2)
        self.assertEqual(np.sum(tst.energy), 10)

        # hour 3.75
        t += dt_sml
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.energy), 11)

        # hour 4
        t += dt_sml
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.energy), 12)

    def test_calc_temporal_superposition(self):
        tol = 0.001

        # 'g' g-functions only
        tst = self.add_instance()

        dt = 900
        t = 0

        tst.aggregate(t, 0)
        tst.aggregate(t, 0)
        hist = tst.calc_temporal_superposition(dt)
        self.assertAlmostEqual(hist, 0, delta=tol)

        t += dt
        tst.aggregate(t, 30000)
        hist = tst.calc_temporal_superposition(dt)
        self.assertAlmostEqual(hist, 19.3806, delta=tol)

        # 'g' and 'g_b' g-functions
        tst = self.add_instance_g_b()

        dt = 900
        t = 0

        tst.aggregate(t, 0)
        tst.aggregate(t, 0)
        hist = tst.calc_temporal_superposition(dt)
        self.assertAlmostEqual(hist, 0, delta=tol)

        t += dt
        tst.aggregate(t, 30000)
        hist = tst.calc_temporal_superposition(dt)
        self.assertAlmostEqual(hist, 38.7612, delta=tol)
