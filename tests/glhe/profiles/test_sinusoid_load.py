import os
import tempfile
import unittest

from math import pi

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.sinusoid_load import SinusoidLoad
from glhe.utilities.functions import write_json


class TestSinusoidLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': [{'load-profile-type': 'sinusoid',
                               'name': 'my name',
                               'amplitude': 1,
                               'offset': 0,
                               'period': 2 * pi}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return SinusoidLoad(d['load-profile'][0], ip, op)

    def test_simulate_time_step(self):
        tol = 0.01

        tst = self.add_instance()

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

    def test_report_output(self):
        tst = self.add_instance()
        d = tst.report_outputs()
        self.assertTrue('SinusoidLoad:MY NAME:Outlet Temp. [C]' in d.keys())
        self.assertTrue('SinusoidLoad:MY NAME:Heat Rate [W]' in d.keys())
