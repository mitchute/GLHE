import unittest

from glhe.globals.functions import get_input_definition_data
from glhe.globals.functions import set_time_step
from glhe.globals.functions import smoothing_function
from glhe.globals.functions import temp_in_kelvin


class TestFunctions(unittest.TestCase):

    def test_smoothing_function(self):
        tolerance = 0.001
        self.assertAlmostEqual(smoothing_function(x=-8, a=0, b=1), 0, delta=tolerance)
        self.assertAlmostEqual(smoothing_function(x=8, a=0, b=1), 1, delta=tolerance)

    def test_temp_in_kelvin(self):
        self.assertEqual(temp_in_kelvin(30), 303.15)

    def test_set_time_step(self):
        self.assertEqual(set_time_step(0), 60)
        self.assertEqual(set_time_step(60), 60)
        self.assertEqual(set_time_step(200), 180)
        self.assertEqual(set_time_step(3500), 3600)

    def test_get_input_definition_data(self):
        tst_def_list = [{"name": "obj 1 name", "param": 1}, {"name": "obj 2 name", "param": 1, "different param": 2}]
        ret_obj = get_input_definition_data(tst_def_list, 'obj 1 name')
        self.assertEqual(ret_obj['name'], 'obj 1 name')
        self.assertEqual(ret_obj['param'], 1)

        ret_obj = get_input_definition_data(tst_def_list, 'obj 2 name')
        self.assertEqual(ret_obj['name'], 'obj 2 name')
        self.assertEqual(ret_obj['param'], 1)
        self.assertEqual(ret_obj['different param'], 2)

        self.assertRaises(ValueError, lambda: get_input_definition_data(tst_def_list, 'not supported name'))
