import os
import tempfile
import unittest

from glhe.gFunction.main import GFunction
from glhe.globals.functions import write_json
from glhe.inputProcessor.processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import TimeStepSimulationResponse


class TestGFunction(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_directory = tempfile.mkdtemp()
        temp_g_function_file = os.path.join(temp_directory, 'g_funcs.csv')
        with open(temp_g_function_file, 'w') as f:
            f.write('1, 1\n2, 2\n3, 3\n')

        d = {
            "borehole-definitions": [
                {
                    "name": "borehole type 1",
                    "depth": 90,
                    "diameter": 0.1099,
                    "grout-type": "standard grout",
                    "model": "simple",
                    "pipe-type": "32 mm SDR-11 HDPE",
                    "segments": 10,
                    "shank-spacing": 0.0521
                }
            ],
            "flow-profile": {
                "type": "fixed",
                "fixed": {
                    "value": 1
                },
                "external": {
                    "path": "./glhe/profiles/external_data"
                }
            },
            "fluid": {
                "type": "water",
                "concentration": 100
            },
            "g-functions": {
                "file": temp_g_function_file,
                "borehole-type": "borehole type 1",
                "number of boreholes": 1
            },
            "ground-temperature": {
                "type": "constant",
                "constant": {
                    "temperature": 20
                },
                "single-harmonic": {
                    "ave-temperature": 20,
                    "amplitude": 0,
                    "phase-shift": 0
                },
                "two-harmonic": {
                    "ave-temperature": 20,
                    "amplitude-1": 10,
                    "amplitude-2": 0,
                    "phase-shift-1": 0,
                    "phase-shift-2": 0
                }
            },
            "grout-definitions": [
                {
                    "name": "standard grout",
                    "conductivity": 0.744,
                    "density": 1500,
                    "specific heat": 2.6
                }
            ],
            "load-aggregation": {
                "type": "dynamic",
                "dynamic": {
                    "param 1": 1
                }
            },
            "pipe-definitions": [
                {
                    "name": "32 mm SDR-11 HDPE",
                    "outer diameter": 0.0334,
                    "inner diameter": 0.0269,
                    "conductivity": 0.389,
                    "density": 950,
                    "specific heat": 1.623
                }
            ],
            "soil": {
                "name": "Some Rock",
                "conductivity": 1.5,
                "density": 1500,
                "specific heat": 1000
            }
        }

        temp_file = os.path.join(temp_directory, 'temp.json')
        write_json(temp_file, d)
        inputs = InputProcessor().process_input(temp_file)
        return GFunction(inputs=inputs)

    def test_class_inheritance(self):
        g = self.add_instance()
        self.assertIsInstance(g, SimulationEntryPoint)

    def test_init_a(self):
        self.add_instance()

    def test_simulate_time_step(self):
        g = self.add_instance()
        response = g.simulate_time_step(inlet_temperature=20.0, mass_flow=0, time_step=15)
        self.assertIsInstance(response, TimeStepSimulationResponse)

    def test_g_function_interp(self):
        g = self.add_instance()
        self.assertEqual(g._g_function_interp(0.5), 0.5)
        self.assertEqual(g._g_function_interp(1.5), 1.5)
        self.assertEqual(g._g_function_interp(2.5), 2.5)
        self.assertEqual(g._g_function_interp(3.5), 3.5)

    def test_get_g_func(self):
        g = self.add_instance()
        self.assertAlmostEqual(g.get_g_func(2446453645.61), 1.0, delta=0.000001)
        self.assertAlmostEqual(g.get_g_func(6650150489.04), 2.0, delta=0.000001)
        self.assertAlmostEqual(g.get_g_func(18076983230.9), 3.0, delta=0.000001)
