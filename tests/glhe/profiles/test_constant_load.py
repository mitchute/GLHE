import os
import tempfile
import unittest

from glhe.utilities.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_load import ConstantLoad


class TestConstantLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': [{'load-profile-type': 'constant', 'name': 'my name', 'value': 4000}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ConstantLoad(d['load-profile'][0], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()

        res = tst.simulate_time_step(SimulationResponse(0, 10, 0, 10))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0)
        self.assertAlmostEqual(res.temperature, 10, delta=0.1)

        res = tst.simulate_time_step(SimulationResponse(0, 10, 0.1, 10))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0.1)
        self.assertAlmostEqual(res.temperature, 19.5, delta=0.1)

    def test_report_outputs(self):
        tst = self.add_instance()
        d = tst.report_outputs()
        self.assertTrue('ConstantLoad:MY NAME:Outlet Temp. [C]' in d.keys())
        self.assertTrue('ConstantLoad:MY NAME:Heat Rate [W]' in d.keys())
