import os
import tempfile
import unittest

from glhe.globals.functions import hanby
from glhe.globals.functions import load_json
from glhe.globals.functions import set_time_step
from glhe.globals.functions import smoothing_function
from glhe.globals.functions import temp_in_kelvin
from glhe.globals.functions import write_json


class TestFunctions(unittest.TestCase):

    def test_smoothing_function(self):
        tolerance = 0.001
        self.assertAlmostEqual(smoothing_function(x=-8, a=0, b=1), 0, delta=tolerance)
        self.assertAlmostEqual(smoothing_function(x=8, a=0, b=1), 1, delta=tolerance)

    def test_temp_in_kelvin(self):
        self.assertEqual(temp_in_kelvin(30), 303.15)

    def test_set_time_step(self):
        self.assertRaises(ZeroDivisionError, lambda: set_time_step(0))
        self.assertEqual(set_time_step(600), 60)
        self.assertEqual(set_time_step(60), 60)
        self.assertEqual(set_time_step(30), 120)
        self.assertEqual(set_time_step(15), 240)
        self.assertEqual(set_time_step(10), 360)
        self.assertEqual(set_time_step(1), 3600)

    def test_load_json(self):
        temp_directory = tempfile.mkdtemp()
        temp_json_file = os.path.join(temp_directory, 'temp.json')
        with open(temp_json_file, 'w') as f:
            f.write('{"key": "value", "key 2": 1}')

        d = load_json(temp_json_file)

        self.assertEqual(d["key"], "value")
        self.assertEqual(d["key 2"], 1)

    def test_write_json(self):
        temp_directory = tempfile.mkdtemp()
        temp_file = os.path.join(temp_directory, 'temp.json')

        d = {
            "key": "value",
            "key 2": 2
        }

        write_json(temp_file, d)
        loaded = load_json(temp_file)
        self.assertEqual(d, loaded)

    def test_hanby(self):
        tolerance = 0.00001
        self.assertAlmostEqual(hanby(0, 1, 1), 0, delta=tolerance)
        self.assertAlmostEqual(hanby(0.3, 1, 1), 0, delta=tolerance)
        self.assertAlmostEqual(hanby(0.5, 1, 1), 0.00345, delta=tolerance)
        self.assertAlmostEqual(hanby(0.8, 1, 1), 0.18775, delta=tolerance)
        self.assertAlmostEqual(hanby(1, 1, 1), 0.52974, delta=tolerance)
        self.assertAlmostEqual(hanby(1.5, 1, 1), 0.97812, delta=tolerance)
