import os
import tempfile
import unittest

from glhe.input_processor.input_processor import InputProcessor
from glhe.input_processor.plant_loop_component_factory import make_plant_loop_component
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.constant_load import ConstantLoad
from glhe.profiles.constant_temp import ConstantTemp
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger
from glhe.topology.pipe import Pipe
from glhe.utilities.functions import write_json

join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


class TestPLCompFactory(unittest.TestCase):

    @staticmethod
    def add_instance():
        f_path = os.path.dirname(os.path.abspath(__file__))
        d = {
            "borehole-definitions": [
                {
                    "borehole-type": "single-grouted",
                    "length": 76.2,
                    "diameter": 0.114,
                    "grout-def-name": "standard grout",
                    "name": "borehole type 1",
                    "pipe-def-name": "26 mm SDR-11 HDPE",
                    "segments": 10,
                    "shank-spacing": 0.0469
                }
            ],
            "borehole": [
                {
                    "name": "bh 1",
                    "borehole-def-name": "borehole type 1",
                    "location": {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    }
                }
            ],
            "flow-profile": [
                {
                    "name": "constant 0.3",
                    "flow-profile-type": "constant",
                    "value": 0.3
                }
            ],
            "fluid": {
                "fluid-type": "water"
            },
            "ground-temperature-model": {
                "ground-temperature-model-type": "constant",
                "temperature": 16.1
            },
            "grout-definitions": [
                {
                    "name": "standard grout",
                    "conductivity": 0.85,
                    "density": 2500,
                    "specific-heat": 1560
                }
            ],
            "load-profile": [
                {
                    "name": "constant 4000",
                    "load-profile-type": "constant",
                    "value": 4000
                }
            ],
            "ground-heat-exchanger": [
                {
                    "name": "GHE 1",
                    "simulation-mode": "enhanced",
                    "g-function-path": norm(join(f_path, '..', '..', '..', 'validation', 'MFRTRT_EWT_g_functions',
                                                 'EWT_experimental_g_functions.csv')),
                    "g_b-function-path": norm(join(f_path, '..', '..', '..', 'validation', 'MFRTRT_EWT_g_functions',
                                                   'EWT_experimental_g_functions.csv')),
                    "flow-paths": [
                        {
                            "name": "path 1",
                            "components": [
                                {
                                    "comp-type": "borehole",
                                    "name": "bh 1"
                                }
                            ]
                        }
                    ],
                    "load-aggregation": {
                        "method": "dynamic",
                        "expansion-rate": 1.5,
                        "number-bins-per-level": 9
                    }
                }
            ],
            "pipe-definitions": [
                {
                    "name": "26 mm SDR-11 HDPE",
                    "outer-diameter": 0.0267,
                    "inner-diameter": 0.0218,
                    "conductivity": 0.39,
                    "density": 950,
                    "specific-heat": 1900
                }
            ],
            'pipe': [
                {'pipe-def-name': '26 mm SDR-11 HDPE',
                 'name': 'pipe 1',
                 'length': 100}],
            "simulation": {
                "name": "Basic GLHE",
                "initial-temperature": 16.1,
                "time-steps-per-hour": 6,
                "runtime": 14400
            },
            "topology": {
                "demand-side": [
                    {
                        "comp-type": "flow-profile",
                        "name": "constant 0.3"
                    },
                    {
                        "comp-type": "load-profile",
                        "name": "constant 4000"
                    }
                ],
                "supply-side": [
                    {
                        "comp-type": "ground-heat-exchanger",
                        "name": "GHE 1"
                    }
                ]
            },
            'temperature-profile': [
                {'temperature-profile-type': 'constant',
                 'name': 'constant 20',
                 'value': 20}],
            "soil": {
                "name": "dirt",
                "conductivity": 2.7,
                "density": 2500,
                "specific-heat": 880
            }
        }

        # adding to debug travis
        g_path = d['ground-heat-exchanger'][0]['g-function-path']
        print("Path: {}".format(g_path))
        print("Path exists: {}".format(os.path.exists(os.path.exists(g_path))))

        temp_dir = tempfile.mkdtemp()
        temp_file = join(temp_dir, 'in.json')
        d['simulation']['output-path'] = temp_dir
        write_json(temp_file, d)
        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')
        return ip, op

    def test_add_flow_profile(self):
        ip, op = self.add_instance()
        tst = make_plant_loop_component({'comp-type': 'flow-profile',
                                         'name': 'constant 0.3'}, ip, op)
        self.assertIsInstance(tst, ConstantFlow)

    def test_add_load_profile(self):
        ip, op = self.add_instance()
        tst = make_plant_loop_component({'comp-type': 'load-profile',
                                         'name': 'constant 4000'}, ip, op)
        self.assertIsInstance(tst, ConstantLoad)

    def test_add_ground_heat_exchanger(self):
        ip, op = self.add_instance()
        tst = make_plant_loop_component({'comp-type': 'ground-heat-exchanger',
                                         'name': 'ghe 1'}, ip, op)
        self.assertIsInstance(tst, GroundHeatExchanger)

    def test_add_pipe(self):
        ip, op = self.add_instance()
        tst = make_plant_loop_component({'comp-type': 'pipe',
                                         'name': 'pipe 1'}, ip, op)
        self.assertIsInstance(tst, Pipe)

    def test_add_temperature_profile(self):
        ip, op = self.add_instance()
        tst = make_plant_loop_component({'comp-type': 'temperature-profile',
                                         'name': 'constant 20'}, ip, op)
        self.assertIsInstance(tst, ConstantTemp)
