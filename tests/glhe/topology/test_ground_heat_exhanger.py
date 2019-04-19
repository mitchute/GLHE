import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger


class TestGroundHeatExchanger(unittest.TestCase):

    @staticmethod
    def add_instance():
        fpath = os.path.dirname(os.path.abspath(__file__))
        d = {
            "borehole-definitions": [
                {
                    "borehole-type": "single-grouted",
                    "depth": 76.2,
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
                    "g-function-path": os.path.join(fpath, '..', '..', '..', 'studies', 'MFRTRT_EWT_g_functions',
                                                    'EWT_experimental_g_functions.csv'),
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
            "soil": {
                "name": "dirt",
                "conductivity": 2.7,
                "density": 2500,
                "specific-heat": 880
            }
        }
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        # op = OutputProcessor(temp_dir, 'out.csv')
        op = OutputProcessor(fpath, 'out.csv')
        return GroundHeatExchanger(d['ground-heat-exchanger'][0], ip, op)

    def test_init(self):
        tst = self.add_instance()
        self.assertIsInstance(tst, GroundHeatExchanger)

    def test_trcm(self):
        tst = self.add_instance()
        tst.generate_trcm_response()
        pass
