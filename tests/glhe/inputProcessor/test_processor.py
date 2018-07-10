import os
import unittest
from contextlib import contextmanager

from jsonschema.exceptions import ValidationError

from glhe.inputProcessor.processor import InputProcessor


class TestInputProcessor(unittest.TestCase):

    @contextmanager
    def assertNotRaise(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))

    def test_validate_pipe_definitions(self):
        d = {
            "pipe-definitions": [{
                "name": "32 mm SDR-11 HDPE",
                "outer diameter": 0.0334,
                "inner diameter": 0.0269,
                "conductivity": 0.389,
                "density": 950,
                "specific heat": 1.623
            }]
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_borehole_definitions(self):
        d = {
            "borehole-definitions": [{
                "name": "borehole type 1",
                "depth": 100,
                "diameter": 0.1099,
                "grout-type": "standard grout",
                "model": "simple",
                "pipe-type": "32 mm SDR-11 HDPE",
                "segments": 10,
                "shank-spacing": 0.0521
            }]
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_grout_definitions(self):
        d = {
            "grout-definitions": [{
                "name": "standard grout",
                "conductivity": 0.744,
                "density": 1500,
                "specific heat": 2.6
            }]
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_flow_profile(self):
        d = {
            "flow-profile": {
                "type": "fixed",
                "fixed": {
                    "value": 1
                },
                "external": {
                    "path": "./glhe/profiles/external_data"
                }}
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_fluid(self):
        d = {
            "fluid": {
                "type": "water",
                "concentration": 100
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_g_functions(self):
        d = {
            "g-functions": {
                "file": "../glhe/examples/2x2_g_functions.csv",
                "average depth": 100,
                "borehole-type": "borehole type 1"
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_ground_temperature(self):
        d = {
            "ground-temperature": {
                "type": "constant",
                "constant": {
                    "temperature": 20
                },
                "single-harmonic": {
                    "ave temperature": 20,
                    "amplitude": 0,
                    "phase shift": 0
                },
                "two-harmonic": {
                    "ave temperature": 20,
                    "amplitude 1": 10,
                    "amplitude 2": 0,
                    "phase-shift 1": 0,
                    "phase-shift 2": 0
                }
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_load_aggregations(self):
        d = {
            "load-aggregation": {
                "type": "dynamic",
                "dynamic": {
                    "param 1": 1
                }
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_load_profile(self):
        d = {
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
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_validate_paths(self):
        d = {
            "paths": [{
                "name": "path 1",
                "boreholes": [{
                    "name": "borehole 1",
                    "location": {
                        "x": 0,
                        "y": 0,
                        "z": 1
                    },
                    "borehole-type": "borehole type 1"
                }]
            }]
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_simulation(self):
        d = {
            "simulation": {
                "name": "Basic GLHE",
                "time-step": 3600,
                "runtime": 31536000,
                "initial-fluid-temperature": 20
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_soil(self):
        d = {
            "soil": {
                "name": "Some Rock",
                "conductivity": 2.4234,
                "density": 1500,
                "specific heat": 1466
            }
        }

        with self.assertNotRaise(ValidationError):
            InputProcessor()._validate_inputs(d)

    def test_all_schema_tests_implemented(self):
        # this count should match the number of schema validations implemented here
        # it will match against the count of all schema files in 'glhe/inputProcessor/schema'
        # not great, but OK for now
        test_count = 12

        fpath = os.path.dirname(os.path.abspath(__file__))
        schema_dir = os.path.normpath(os.path.join(fpath, '..', '..', '..', 'glhe', 'inputProcessor', 'schema'))
        schema_count = len([name for name in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, name))])
        self.assertEqual(test_count, schema_count)
