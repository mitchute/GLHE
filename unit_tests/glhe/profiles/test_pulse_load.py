import os
import tempfile
import unittest

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.pulse_load import PulseLoad
from glhe.utilities.functions import write_json


class TestImpulseLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': [{'load-profile-type': 'single-impulse',
                               'name': 'my name',
                               'value': 1000,
                               'start-time': 0,
                               'end-time': 200}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return PulseLoad(d['load-profile'][0], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()

        res = tst.simulate_time_step(SimulationResponse(0, 10, 0, 10))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0)
        self.assertAlmostEqual(res.temperature, 10, delta=0.1)

        res = tst.simulate_time_step(SimulationResponse(0, 10, 0.01, 10))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0.01)
        self.assertAlmostEqual(res.temperature, 33.8, delta=0.1)

        res = tst.simulate_time_step(SimulationResponse(300, 10, 0.01, 10))
        self.assertEqual(res.time, 300)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0.01)
        self.assertEqual(res.temperature, 10)

    def test_report_outputs(self):
        tst = self.add_instance()
        d = tst.report_outputs()
        self.assertTrue('PulseLoad:MY NAME:Outlet Temp. [C]' in d.keys())
        self.assertTrue('PulseLoad:MY NAME:Heat Rate [W]' in d.keys())
