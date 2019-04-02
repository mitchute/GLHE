import os
import tempfile
import unittest

from math import log

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.pipe import Pipe


class TestPipe(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {'pipe-definitions': [{
            'name': '32 mm sdr-11 hdpe',
            'outer-diameter': 0.0334,
            'inner-diameter': 0.0269,
            'conductivity': 0.389,
            'density': 950,
            'specific-heat': 1900}],
            'fluid': {'fluid-type': 'water'},
            'pipe': [
                {'pipe-def-name': '32 mm sdr-11 hdpe',
                 'name': 'pipe 1',
                 'length': 100}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, inputs)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return Pipe(inputs['pipe'][0], ip, op)

    def test_calc_friction_factor(self):
        tst = self.add_instance()
        tolerance = 0.00001

        # laminar tests
        re = 100  # noqa: E126
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1000
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1400
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.034003503, delta=tolerance)

        re = 3000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.033446219, delta=tolerance)

        re = 4000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.03895358, delta=tolerance)

        # turbulent tests
        re = 5000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 15000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 25000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

    def test_calc_conduction_resistance(self):
        tst = self.add_instance()
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_cond_resist(), 0.088549, delta=tolerance)

    def test_calc_convection_resistance(self):
        tst = self.add_instance()
        temp = 20
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_conv_resist(0, temp), 0.13273, delta=tolerance)
        self.assertAlmostEqual(tst.calc_conv_resist(0.07, temp), 0.02645, delta=tolerance)
        self.assertAlmostEqual(tst.calc_conv_resist(2, temp), 0.00094, delta=tolerance)

    def test_calc_resistance(self):
        tst = self.add_instance()
        temp = 20
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_resist(0, temp), 0.22128, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resist(0.07, temp), 0.11500, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resist(2, temp), 0.08948, delta=tolerance)

    def test_set_resistance(self):
        tst = self.add_instance()
        tst.set_resist(1)
        self.assertEqual(tst.resist_pipe, 1)

    def test_calc_transit_time(self):
        tst = self.add_instance()
        tol = 0.1
        self.assertAlmostEqual(tst.calc_transit_time(0.1, 20), 567.3, delta=tol)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        for t in range(0, 800, 100):
            tst.simulate_time_step(SimulationResponse(t, 100, 0.1, 25))
