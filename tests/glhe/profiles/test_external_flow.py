import os
import tempfile
import unittest

from glhe.utilities.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_flow import ExternalFlow


class TestExternalFlow(unittest.TestCase):

    @staticmethod
    def add_instance(path):
        d = {'flow-profile': [{'flow-profile-type': 'external', 'name': 'my name', 'path': path}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return ExternalFlow(d['flow-profile'][0], ip, op)

    def test_get_value(self):
        dir_name = os.path.dirname(__file__)
        relative_path = '../../../glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv'
        path = os.path.normpath(os.path.join(dir_name, relative_path))
        tst = self.add_instance(path)
        self.assertEqual(tst.get_value(0), 0)
        self.assertEqual(tst.get_value(10 * 3600), 1)
        self.assertEqual(tst.get_value(8759 * 3600), 0)

    def test_start_end_points(self):
        temp_dir = tempfile.mkdtemp()
        temp_data = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_data, 'w') as f:
            f.write('Date/Time, Meas. Total Power [W], mdot [kg/s]\n'
                    '2018-01-01 00:00:00, 1, 1\n'
                    '2018-01-01 01:00:00, 2, 2\n'
                    '2018-01-01 02:00:00, 3, 3\n'
                    '2018-01-01 03:00:00, 4, 4\n')

        tst = self.add_instance(temp_data)

        self.assertEqual(tst.get_value(0.0), 1.0)
        self.assertEqual(tst.get_value(1.0 * 3600), 2.0)
        self.assertEqual(tst.get_value(1.5 * 3600), 2.5)
        self.assertEqual(tst.get_value(2.0 * 3600), 3.0)
        self.assertEqual(tst.get_value(3.0 * 3600), 4.0)

    def test_repeated_points(self):
        temp_dir = tempfile.mkdtemp()
        temp_data = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_data, 'w') as f:
            f.write('Date/Time, Meas. Total Power [W], mdot [kg/s]\n'
                    '2018-01-01 00:00:00, 1, 1\n'
                    '2018-01-01 01:00:00, 2, 2\n'
                    '2018-01-01 02:00:00, 3, 3\n'
                    '2018-01-01 03:00:00, 4, 4\n')

        tst = self.add_instance(temp_data)

        self.assertEqual(tst.get_value(4.0 * 3600), 1.0)
        self.assertEqual(tst.get_value(4.5 * 3600), 1.5)
        self.assertEqual(tst.get_value(5.0 * 3600), 2.0)
        self.assertEqual(tst.get_value(6.0 * 3600), 3.0)
        self.assertEqual(tst.get_value(7.0 * 3600), 4.0)
        self.assertEqual(tst.get_value(8.0 * 3600), 1.0)
        self.assertEqual(tst.get_value(9.0 * 3600), 2.0)
        self.assertEqual(tst.get_value(10.0 * 3600), 3.0)
        self.assertEqual(tst.get_value(11.0 * 3600), 4.0)
        self.assertEqual(tst.get_value(12.0 * 3600), 1.0)

    def test_simulate_time_step(self):
        temp_dir = tempfile.mkdtemp()
        temp_data = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_data, 'w') as f:
            f.write('Date/Time, Meas. Total Power [W], mdot [kg/s]\n'
                    '2018-01-01 00:00:00, 1, 1\n'
                    '2018-01-01 01:00:00, 2, 2\n'
                    '2018-01-01 02:00:00, 3, 3\n'
                    '2018-01-01 03:00:00, 4, 4\n')

        tst = self.add_instance(temp_data)
        res = tst.simulate_time_step(SimulationResponse(0, 3600, 0.00001, 10))
        self.assertEqual(res.time, 0)
        self.assertEqual(res.time_step, 3600)
        self.assertEqual(res.flow_rate, 2)
        self.assertEqual(res.temperature, 10)

    def test_report_outputs(self):
        temp_dir = tempfile.mkdtemp()
        temp_data = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_data, 'w') as f:
            f.write('Date/Time, Meas. Total Power [W], mdot [kg/s]\n'
                    '2018-01-01 00:00:00, 1, 1\n'
                    '2018-01-01 01:00:00, 2, 2\n'
                    '2018-01-01 02:00:00, 3, 3\n'
                    '2018-01-01 03:00:00, 4, 4\n')

        tst = self.add_instance(temp_data)
        d = tst.report_outputs()
        self.assertTrue('ExternalFlow:MY NAME:Flow Rate [kg/s]' in d.keys())
