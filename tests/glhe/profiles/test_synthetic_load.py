import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.synthetic_load import SyntheticLoad


class TestSynthetic(unittest.TestCase):

    @staticmethod
    def add_instance(method):
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': {'load-profile-type': 'synthetic',
                              'amplitude': 1000,
                              'synthetic-method': method}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return SyntheticLoad(d['load-profile'], ip, op)

    def test_get_value(self):
        tol = 1e-1
        tst = self.add_instance('asymmetric')
        self.assertAlmostEqual(tst.get_value(0), -139.91, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), 0.3038, delta=tol)

        tst = self.add_instance('symmetric')
        self.assertAlmostEqual(tst.get_value(0), -0.01, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), -0.01, delta=tol)
