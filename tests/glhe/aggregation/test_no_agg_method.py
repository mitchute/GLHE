import unittest

import numpy as np

from glhe.aggregation.no_agg import NoAgg


class TestNoAgg(unittest.TestCase):

    def test_aggregate(self):
        tst = NoAgg()

        dt = 900
        t = 0

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 1)

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 2)
