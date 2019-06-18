import os
import tempfile
import unittest

from glhe.utilities.functions import load_json
from glhe.utilities.functions import write_json
from standalone.plant_loop import PlantLoop

norm = os.path.normpath
join = os.path.join


class TestPlantLoop(unittest.TestCase):

    def setUp(self):
        self.this_file_directory = os.path.dirname(os.path.realpath(__file__))

    def test_simulate(self):
        temp_dir = tempfile.mkdtemp()
        temp_file = join(temp_dir, 'in.json')
        input_path = norm(join(self.this_file_directory, '..', '..', 'test_files', 'single.json'))
        d = load_json(input_path)
        g_path = norm(join(self.this_file_directory, '..', '..', 'test_files', 'single_g_functions.csv'))
        d['ground-heat-exchanger'][0]['g-function-path'] = g_path
        d['simulation']['output-path'] = temp_dir
        write_json(temp_file, d)
        p = PlantLoop(temp_file)
        self.assertTrue(p.simulate())
