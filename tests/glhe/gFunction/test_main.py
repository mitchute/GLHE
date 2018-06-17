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
                'average-depth': 20,
            },
            'soil': {
                'conductivity': 1,
                'density': 2,
                'specific heat': 3,
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
