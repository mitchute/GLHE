import os
import tempfile
import unittest

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.utilities.functions import write_json


class TestConstantFlow(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'flow-profile': [{'flow-profile-type': 'constant', 'name': 'my name', 'value': 0.1}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ConstantFlow(d['flow-profile'][0], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        res = tst.simulate_time_step(SimulationResponse(0, 10, 0, 10))

        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0.1)
        self.assertEqual(res.temperature, 10)

    def test_report_outputs(self):
        tst = self.add_instance()
        d = tst.report_outputs()
        self.assertTrue('ConstantFlow:MY NAME:Flow Rate [kg/s]' in d.keys())
