from json import loads
from pathlib import Path
import tempfile
import unittest

from glhe.functions import write_json
from glhe.standalone.plant_loop import PlantLoop


class TestPlantLoop(unittest.TestCase):

    def setUp(self):
        self.this_file_directory = Path(__file__).parent

    def test_simulate(self):
        temp_dir = Path(tempfile.mkdtemp())
        temp_file = temp_dir / 'in.json'
        input_path = self.this_file_directory.parent.parent / 'test_files' / 'single.json'
        d = loads(input_path.read_text())
        g_path = self.this_file_directory.parent.parent / 'test_files' / 'single_g_functions.csv'
        d['ground-heat-exchanger'][0]['g-function-path'] = str(g_path)
        d['simulation']['output-path'] = str(temp_dir)
        write_json(temp_file, d)
        p = PlantLoop(temp_file)
        self.assertTrue(p.simulate())
