import os
import tempfile
import unittest

import numpy as np

from glhe.aggregation.no_agg import NoAgg


class TestNoAgg(unittest.TestCase):

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

        d = {'method': 'none',
             'time-scale': 5e9,
             'g-function-path': temp_csv}

        return NoAgg(d)

    def test_aggregate(self):
        tst = self.add_instance()

        dt = 900
        t = 0

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.energy), 1)

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.energy), 2)

    def test_calc_superposition_coeffs(self):
        tol = 0.001

        tst = self.add_instance()

        dt = 900
        t = 0

        tst.aggregate(t, 0)
        tst.aggregate(t, 0)
        g, hist = tst.calc_superposition_coeffs(t, dt)
        self.assertAlmostEqual(g, 0.2348, delta=tol)
        self.assertAlmostEqual(hist, 0, delta=tol)

        t += dt
        tst.aggregate(t, 30000)
        g, hist = tst.calc_superposition_coeffs(t, dt)
        self.assertAlmostEqual(g, 0.2348, delta=tol)
        self.assertAlmostEqual(hist, 11.5524, delta=tol)
