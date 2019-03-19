import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_load import ConstantLoad


class TestConstantLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': {'load-profile-type': 'constant', 'value': 4000}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ConstantLoad(d['load-profile'], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        res = tst.simulate_time_step(SimulationResponse(0, 10, 0.1, 10))

        self.assertEqual(res.sim_time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.mass_flow_rate, 0.1)
        self.assertAlmostEqual(res.temperature, 19.5, delta=0.1)
