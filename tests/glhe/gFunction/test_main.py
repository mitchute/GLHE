import os
import tempfile
import unittest

from glhe.gFunction.main import GFunction
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse


class TestGFunction(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_directory = tempfile.mkdtemp()
        temp_g_function_file = os.path.join(temp_directory, 'g_funcs.csv')
        with open(temp_g_function_file, 'w') as f:
            f.write('1, 1\n2, 2\n3, 3\n')
        input_structure = {
            'g-functions': {
                'file': temp_g_function_file,
                'average-depth': 90,
            },
            'soil': {
                'conductivity': 1.5,
                'density': 1500,
                'specific heat': 1000,
            },
            'load-aggregation': {
                'type': 'dynamic'
            },
            'simulation': {
                "ground-temperature": {
                    "type": "constant",
                    "constant": {
                        "temperature": 20}
                }
            }
        }

        return GFunction(inputs=input_structure)

    def test_class_inheritance(self):
        g = self.add_instance()
        self.assertIsInstance(g, SimulationEntryPoint)

    def test_init_a(self):
        self.add_instance()

    def test_simulate_time_step(self):
        g = self.add_instance()
        response = g.simulate_time_step(inlet_temperature=20.0, flow=1.0, time_step=15)
        self.assertIsInstance(response, TimeStepSimulationResponse)
        self.assertAlmostEqual(response.outlet_temperature, 20.0, 2)

    def test_g_function_interp(self):
        g = self.add_instance()
        self.assertEqual(g._g_function(0.5), 0.5)
        self.assertEqual(g._g_function(1.5), 1.5)
        self.assertEqual(g._g_function(2.5), 2.5)
        self.assertEqual(g._g_function(3.5), 3.5)

    def test_get_g_func(self):
        g = self.add_instance()
        self.assertAlmostEqual(g.get_g_func(2446453645.61), 1.0, delta=0.000001)
        self.assertAlmostEqual(g.get_g_func(6650150489.04), 2.0, delta=0.000001)
        self.assertAlmostEqual(g.get_g_func(18076983230.9), 3.0, delta=0.000001)
