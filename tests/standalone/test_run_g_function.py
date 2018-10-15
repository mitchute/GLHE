import os
import tempfile
import unittest

import pandas as pd

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

        temp_directory = tempfile.mkdtemp()
        temp_file = os.path.join(temp_directory, 'temp.json')

        input_dict = load_json(input_file_path)
        input_dict['load-aggregation']['type'] = agg_method
        input_dict['g-functions']['file'] = g_function_path
        input_dict['simulation']['time-steps per hour'] = 1
        input_dict['simulation']['runtime'] = 86400
        input_dict['simulation']['output-path'] = os.path.join(temp_directory, 'out.csv')

        write_json(temp_file, input_dict)

        return RunGFunctions(temp_file), input_dict['simulation']['output-path']

    def test_no_agg(self):
        tst, path = self.add_instance('none')
        tst.simulate()
        df = pd.read_csv(path)
        self.assertAlmostEqual(df['GLHE Outlet Temperature [C]'].iloc[-1], 30.76, delta=0.15)

    def test_static_agg(self):
        tst, path = self.add_instance('static')
        tst.simulate()
        df = pd.read_csv(path)
        self.assertAlmostEqual(df['GLHE Outlet Temperature [C]'].iloc[-1], 30.76, delta=0.15)

    def test_dynamic_agg(self):
        tst, path = self.add_instance('dynamic')
        tst.simulate()
        df = pd.read_csv(path)
        self.assertAlmostEqual(df['GLHE Outlet Temperature [C]'].iloc[-1], 30.9, delta=0.15)
