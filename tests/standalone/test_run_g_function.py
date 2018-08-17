import os
import tempfile
import unittest

from glhe.globals.functions import load_json
from glhe.globals.functions import write_json
from standalone.run_g_function import RunGFunctions


class TestRunGFunctionIntegration(unittest.TestCase):

    @staticmethod
    def add_instance(agg_method):
        dir_name = os.path.dirname(__file__)
        relative_path = "../../glhe/examples"
        input_file_path = os.path.normpath(os.path.join(dir_name, relative_path, 'single.json'))
        g_function_path = os.path.normpath(os.path.join(dir_name, relative_path, 'single_g_functions.csv'))

        input_dict = load_json(input_file_path)

        input_dict['load-aggregation']['type'] = agg_method
        input_dict['g-functions']['file'] = g_function_path
        input_dict['simulation']['time-steps per hour'] = 1
        input_dict['simulation']['runtime'] = 86400

        temp_directory = tempfile.mkdtemp()
        temp_file = os.path.join(temp_directory, 'temp.json')
        write_json(temp_file, input_dict)

        return RunGFunctions(temp_file)

    def test_no_agg(self):
        tst = self.add_instance('none')
        tst.simulate()

    def test_static_agg(self):
        tst = self.add_instance('static')
        tst.simulate()

    def test_dynamic_agg(self):
        tst = self.add_instance('dynamic')
        tst.simulate()
