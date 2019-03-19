import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.impulse_load import ImpulseLoad


class TestImpulseLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': {'load-profile-type': 'single-impulse', 'value': 1000, 'start-time': 0, 'end-time': 200}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ImpulseLoad(d['load-profile'], ip, op)

    def test_get_value(self):
        tst = self.add_instance()
        res = tst.simulate_time_step(SimulationResponse(0, 10, 0.01, 10))
        self.assertEqual(res.sim_time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.mass_flow_rate, 0.01)
        self.assertAlmostEqual(res.temperature, 33.8, delta=0.1)

        res = tst.simulate_time_step(SimulationResponse(300, 10, 0.01, 10))
        self.assertEqual(res.sim_time, 300)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.mass_flow_rate, 0.01)
        self.assertEqual(res.temperature, 10)
