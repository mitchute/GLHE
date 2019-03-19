import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_flow import ConstantFlow


class TestConstantFlow(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'flow-profile': {'load-profile-type': 'constant', 'value': 0.1}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ConstantFlow(d['flow-profile'], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        res = tst.simulate_time_step(SimulationResponse(0, 10, 0, 10))

        self.assertEqual(res.sim_time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.mass_flow_rate, 0.1)
        self.assertEqual(res.temperature, 10)
