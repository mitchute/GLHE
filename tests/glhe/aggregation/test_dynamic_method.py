import unittest

import numpy as np

from glhe.aggregation.dynamic import Dynamic


class TestDynamic(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'method': 'dynamic', 'expansion-rate': 2, 'number-bins-per-level': 2, 'runtime': 36000}
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
