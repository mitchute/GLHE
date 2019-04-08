import unittest

import numpy as np

from glhe.aggregation.no_agg_method import NoAggMethod


class TestNoAgg(unittest.TestCase):

    def test_aggregate(self):
        tst = NoAggMethod()

        dt = 900
        t = 0

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 1)

        t += dt
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 2)
