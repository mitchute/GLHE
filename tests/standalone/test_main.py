import unittest

from glhe.topology.full_ground_loop import GLHE


class TestGLHEIntegration(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {
            'soil': {
                'conductivity': 1.5,
                'density': 1500,
                'specific heat': 1000,
            },
            "fluid": {
                "type": "water",
                "concentration": 100
            },
            'load-aggregation': {
                'type': 'dynamic'
            },
            "ground-temperature": {
                "type": "constant",
                "constant": {
                    "temperature": 20
                },
            },
            "borehole-definitions": [
                {
                    "name": "borehole type 1",
                    "depth": 100,
                    "diameter": 0.1099,
                    "shank-spacing": 0.0521,
                    "grout-type": "standard grout",
                    "pipe-type": "32 mm SDR-11 HDPE",
                    "segments": 10,
                    "model-type": "simple"
                }
            ],
            "grout-definitions": [
                {
                    "name": "standard grout",
                    "conductivity": 0.744,
                    "density": 1500,
                    "specific heat": 2.6
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
            "paths": [
                {
                    "name": "path 1",
                    "boreholes": [
                        {
                            "name": "borehole 1",
                            "location": {
                                "x": 0,
                                "y": 0,
                                "z": 1
                            },
                            "borehole-type": "borehole type 1"
                        },
                        {
                            "name": "borehole 2",
                            "location": {
                                "x": 1,
                                "y": 0,
                                "z": 1
                            },
                            "borehole-type": "borehole type 1"
                        }
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
            "simulation": {
                "name": "Basic GLHE",
                "time-step": 3600,
                "runtime": 31536000,
                "initial-fluid-temperature": 20
            }
        }

        return GLHE(inputs=inputs)

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst.simulate_time_step(20, 1, 300), None)
