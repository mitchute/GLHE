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
            "borehole-definitions": {
                "types": [
                    {
                        "type": "borehole type 1",
                        "depth": 100,
                        "diameter": 0.1099,
                        "grout-type": "standard grout",
                        "model": "simple",
                        "pipe-type": "32 mm SDR-11 HDPE",
                        "segments": 10,
                        "shank-spacing": 0.0521
                    }
                ],
                "instances": [
                    {
                        "name": "fancy borehole name",
                        "location": (1, 2, 3),
                        "type": "borehole type 1"
                    },
                ]
            },
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
                "average-depth": 100,
                "borehole-name": "fancy borehole name"  # FULLY QUALIFIED BOREHOLE
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
            "load-profile": {
                "type": "fixed",
                "fixed": {
                    "value": 2000
                },
                "single-impulse": {
                    "start-time": 100,
                    "end-time": 200,
                    "value": 3000
                },
                "external": {
                    "path": "./glhe/profiles/external_data"
                },
                "sinusoid": {
                    "amplitude": 1000,
                    "offset": 0,
                    "period": 0
                },
                "synthetic": {
                    "type": "symmetric",
                    "amplitude": 1000
                }
            },
            "paths": [
                {
                    "name": "path 1",
                    "boreholes": [
                        "fancy borehole name",  # BECOMES A FULL BOREHOLE REPRESENTATION
                        "fancy borehole name 2"
                    ]
                },
                {
                    "name": "path 2",
                    "boreholes": [
                        {
                            "name": "borehole 3",
                            "location": {
                                "x": 0,
                                "y": 1,
                                "z": 1
                            },
                            "borehole-type": "borehole type 1"
                        },
                        {
                            "name": "borehole 4",
                            "location": {
                                "x": 1,
                                "y": 1,
                                "z": 1
                            },
                            "borehole-type": "borehole type 1"
                        }
                    ]
                }
            ],
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
            "simulation": {
                "name": "Basic GLHE",
                "time-step": 3600,
                "runtime": 31536000,
                "initial-fluid-temperature": 20
            },
            "soil": {
                "name": "Some Rock",
                "conductivity": 2.4234,
                "density": 1500,
                "specific heat": 1466
            }
        }

        # d = {
        #     'g-functions': {
        #         'file': temp_g_function_file,
        #         'average-depth': 90,
        #         'borehole-type': 'borehole type 1'
        #     },
        #     'soil': {
        #         'conductivity': 1.5,
        #         'density': 1500,
        #         'specific heat': 1000,
        #     },
        #     "fluid": {
        #         "type": "water",
        #         "concentration": 100
        #     },
        #     'load-aggregation': {
        #         'type': 'dynamic'
        #     },
        #     "ground-temperature": {
        #         "type": "constant",
        #         "constant": {
        #             "temperature": 20
        #         },
        #     },
        #     "borehole-definitions": [
        #         {
        #             "name": "borehole type 1",
        #             "depth": 100,
        #             "diameter": 0.1099,
        #             "shank-spacing": 0.0521,
        #             "grout-type": "standard grout",
        #             "pipe-type": "32 mm SDR-11 HDPE",
        #             "segments": 10,
        #             "model-type": "simple"
        #         }
        #     ],
        #     "grout-definitions": [
        #         {
        #             "name": "standard grout",
        #             "conductivity": 0.744,
        #             "density": 1500,
        #             "specific heat": 2.6
        #         }
        #     ],
        #     "pipe-definitions": [
        #         {
        #             "name": "32 mm SDR-11 HDPE",
        #             "outer diameter": 0.0334,
        #             "inner diameter": 0.0269,
        #             "conductivity": 0.389,
        #             "density": 950,
        #             "specific heat": 1.623
        #         }
        #     ]
        # }

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
