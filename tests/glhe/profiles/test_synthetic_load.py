import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.synthetic_load import SyntheticLoad


class TestSynthetic(unittest.TestCase):

    @staticmethod
    def add_instance(method):
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': [{'load-profile-type': 'synthetic',
                               'name': 'my name',
                               'amplitude': 1000,
                               'synthetic-method': method}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return SyntheticLoad(d['load-profile'][0], ip, op)

    def test_get_value(self):
        tol = 1e-1
        tst = self.add_instance('asymmetric')
        self.assertAlmostEqual(tst.get_value(0), -139.91, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), 0.3038, delta=tol)

        tst = self.add_instance('symmetric')
        self.assertAlmostEqual(tst.get_value(0), -0.01, delta=tol)
        self.assertAlmostEqual(tst.get_value(2190), -0.01, delta=tol)

    def test_simulate_time_step(self):
        tol = 0.01

        tst = self.add_instance('symmetric')

        res = tst.simulate_time_step(SimulationResponse(0, 60, 0, 20))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 60)
        self.assertEqual(res.flow_rate, 0)
        self.assertEqual(res.temperature, 20)

        res = tst.simulate_time_step(SimulationResponse(0, 60, 0.2, 20))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 60)
        self.assertEqual(res.flow_rate, 0.2)
        self.assertAlmostEqual(res.temperature, 20, delta=tol)

    def test_report_outputs(self):
        tst = self.add_instance('symmetric')
        d = tst.report_outputs()
        self.assertTrue('SyntheticLoad:MY NAME:Outlet Temp [C]' in d.keys())
        self.assertTrue('SyntheticLoad:MY NAME:Heat Rate [W]' in d.keys())

    def test_fail(self):
        with self.assertRaises(ValueError) as _:
            self.add_instance('not-a-method')
