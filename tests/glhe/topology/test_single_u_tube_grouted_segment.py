import os
import tempfile
import unittest

from glhe.utilities.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment


class TestSingleUTubeGroutedSegment(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {
            'fluid': {'fluid-type': 'water'},

            'soil': {
                "name": "dirt",
                "conductivity": 2.7,
                "density": 2500,
                "specific-heat": 880
            },

            'grout-definitions': [{
                'name': 'standard grout',
                'conductivity': 0.744,
                'density': 1500,
                'specific-heat': 800}],

            'pipe-definitions': [{
                'name': '32 mm SDR-11 HDPE',
                'outer-diameter': 0.0334,
                'inner-diameter': 0.0269,
                'conductivity': 0.389,
                'density': 950,
                'specific-heat': 1900}]
        }

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        d_seg = {'length': 7.62,
                 'diameter': 0.114,
                 'segment-name': 0,
                 'grout-def-name': 'standard grout',
                 'pipe-def-name': '32 mm sdr-11 hdpe'}

        return SingleUTubeGroutedSegment(d_seg, ip, op)

    def test_volume(self):
        tst = self.add_instance()
        tol = 0.0001

        self.assertAlmostEqual(tst.calc_grout_volume(), 0.064424943, delta=tol)
        self.assertAlmostEqual(tst.calc_seg_volume(), 0.077777603, delta=tol)
        self.assertAlmostEqual(tst.calc_tot_pipe_volume(), 0.01335266, delta=tol)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        inputs = {'boundary-temperature': 20,
                  'inlet-1-temp': 30,
                  'inlet-2-temp': 25,
                  'flow-rate': 0.2,
                  'rb': 0.16,
                  'dc-resist': 2.28}

        ret_temps = tst.simulate_time_step(1, inputs)

        tol = 0.0001
        self.assertAlmostEqual(ret_temps[0], 20.4525, delta=tol)
        self.assertAlmostEqual(ret_temps[1], 20.2262, delta=tol)
        self.assertAlmostEqual(ret_temps[2], 20.0002, delta=tol)
        self.assertAlmostEqual(ret_temps[3], 20.0002, delta=tol)
