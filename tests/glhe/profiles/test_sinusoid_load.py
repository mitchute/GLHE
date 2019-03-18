import os
import tempfile
import unittest
from math import pi

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.sinusoid_load import SinusoidLoad


class TestSinusoidLoad(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'fluid': {'fluid-type': 'water'},
             'load-profile': {'load-profile-type': 'sinusoid',
                              'amplitude': 1,
                              'offset': 0,
                              'period': 2 * pi}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return SinusoidLoad(d['load-profile'], ip, op)

    def test_simulate_time_step(self):
        tol = 1e-10

        tst = self.add_instance()
        self.assertAlmostEqual(tst.get_value(0), 0, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi / 2), 1, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi), 0, delta=tol)
        self.assertAlmostEqual(tst.get_value(pi * 3 / 2), -1, delta=tol)
        self.assertAlmostEqual(tst.get_value(2 * pi), 0, delta=tol)
