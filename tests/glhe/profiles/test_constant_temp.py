import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_temp import ConstantTemp


class TestConstantFlow(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'temperature-profile': [{'temperature-profile-type': 'constant', 'name': 'my name', 'value': 20}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ConstantTemp(d['temperature-profile'][0], ip, op)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        res = tst.simulate_time_step(SimulationResponse(0, 10, 0, 10))

        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 10)
        self.assertEqual(res.flow_rate, 0)
        self.assertEqual(res.temperature, 20)

    def test_report_outputs(self):
        tst = self.add_instance()
        d = tst.report_outputs()
        self.assertTrue('ConstantTemp:MY NAME:Inlet Temp. [C]' in d.keys())
        self.assertTrue('ConstantTemp:MY NAME:Outlet Temp. [C]' in d.keys())
