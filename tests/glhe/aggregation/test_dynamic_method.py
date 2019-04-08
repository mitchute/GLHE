import os
import tempfile
import unittest

import numpy as np

from glhe.aggregation.agg_method_factory import make_agg_method
from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor


class TestDynamic(unittest.TestCase):

    @staticmethod
    def add_instance():
        d_to_file = {'simulation': {'name': 'test dynamic',
                                    'initial-temperature': 16,
                                    'time-steps-per-hour': 60,
                                    'runtime': 36000}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d_to_file)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        d = {'method': 'dynamic', 'expansion-rate': 2, 'number-bins-per-level': 2}

        return make_agg_method(d, ip, op)

    def test_aggregate(self):
        tst = self.add_instance()

        dt_lrg = 3600
        dt_med = 1800
        dt_sml = 900
        t = 0

        # hour 1
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.loads), 0)

        # hour 2
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.loads), 4)

        # hour 3
        t += dt_lrg
        tst.aggregate(t, 4)
        self.assertEqual(np.sum(tst.loads), 8)

        # hour 3.5
        t += dt_med
        tst.aggregate(t, 2)
        self.assertEqual(np.sum(tst.loads), 10)

        # hour 3.75
        t += dt_sml
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 11)

        # hour 4
        t += dt_sml
        tst.aggregate(t, 1)
        self.assertEqual(np.sum(tst.loads), 12)
