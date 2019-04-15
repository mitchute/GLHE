import os
import tempfile
import unittest
from contextlib import contextmanager

from jsonschema.exceptions import ValidationError

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor


class TestInputProcessor(unittest.TestCase):

    @contextmanager
    def assertNotRaise(self, exc_type):
        try:
            yield None
        except exc_type:  # pragma: no cover
            raise self.failureException('{} raised'.format(exc_type.__name__))  # pragma: no cover

    def run_validate(self, inputs):
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, inputs)

        with self.assertNotRaise(ValidationError):
            InputProcessor(temp_file)

    def test_validate_pipe_definitions(self):
        d = {'pipe-definitions': [{
            'name': '32 mm SDR-11 HDPE',
            'outer-diameter': 0.0334,
            'inner-diameter': 0.0269,
            'conductivity': 0.389,
            'density': 950,
            'specific-heat': 1900}]}

        self.run_validate(d)

    def test_validate_borehole_definitions(self):
        d = {'borehole-definitions': [{
            'borehole-type': 'single-grouted',
            'name': 'borehole type 1',
            'depth': 100,
            'diameter': 0.1099,
            'grout-def-name': 'standard grout',
            'pipe-def-name': '32 mm SDR-11 HDPE',
            'segments': 10,
            'shank-spacing': 0.0521}]}

        self.run_validate(d)

    def test_validate_grout_definitions(self):
        d = {'grout-definitions': [{
            'name': 'standard grout',
            'conductivity': 0.744,
            'density': 1500,
            'specific-heat': 800}]}

        self.run_validate(d)

    def test_validate_flow_profile(self):
        d = {'flow-profile': [
            {'flow-profile-type': 'constant',
             'name': 'constant',
             'value': 1}]}

        self.run_validate(d)

        d = {'flow-profile': [
            {'flow-profile-type': 'external',
             'name': 'from ext file',
             'path': 'some/path/to/file'}]}

        self.run_validate(d)

    def test_validate_fluid(self):
        d = {'fluid': {'fluid-type': 'water'}}

        self.run_validate(d)

        d = {'fluid': {'fluid-type': 'EA', 'concentration': 100}}

        self.run_validate(d)

        d = {'fluid': {'fluid-type': 'EG', 'concentration': 100}}

        self.run_validate(d)

        d = {'fluid': {'fluid-type': 'PG', 'concentration': 100}}

        self.run_validate(d)

    def test_validate_ground_temperature(self):
        d = {'ground-temperature-model': {'ground-temperature-model-type': 'constant',
                                          'temperature': 10}}

        self.run_validate(d)

        d = {'ground-temperature-model': {'ground-temperature-model-type': 'single-harmonic',
                                          'average-temperature': 10,
                                          'amplitude': 10,
                                          'phase-shift': 10}}

        self.run_validate(d)

        d = {'ground-temperature-model': {'ground-temperature-model-type': 'two-harmonic',
                                          'average-temperature': 10,
                                          'amplitude-1': 10,
                                          'amplitude-2': 10,
                                          'phase-shift-1': 10,
                                          'phase-shift-2': 10}}

        self.run_validate(d)

    def test_load_profile(self):
        d = {'load-profile': [{'load-profile-type': 'constant',
                               'value': 2000}]}

        self.run_validate(d)

        d = {'load-profile': [{'load-profile-type': 'single-impulse',
                               'value': 2000,
                               'start-time': 0,
                               'end-time': 3600}]}

        self.run_validate(d)

        d = {'load-profile': [{'load-profile-type': 'external',
                               'path': 'some/path'}]}

        self.run_validate(d)

        d = {'load-profile': [{'load-profile-type': 'sinusoid',
                               'amplitude': 10,
                               'offset': 10,
                               'period': 10}]}

        self.run_validate(d)

        d = {'load-profile': [{'load-profile-type': 'synthetic',
                               'synthetic-method': 'symmetric',
                               'amplitude': 10}]}

        self.run_validate(d)

    def test_validate_ground_heat_exchanger(self):
        d = {"ground-heat-exchanger": [{
            "name": "GHE 1",
            "g-function-path": "../glhe/examples/single_g_functions.csv",
            "flow-paths": [
                {"path-name": "path 1",
                 "components": [{"comp-type": "borehole", "def-name": "borehole type 1", "name": "BH 1"}]},
                {"path-name": "path 2",
                 "components": [{"comp-type": "borehole", "def-name": "borehole type 1", "name": "BH 3"}]}],
            "load-aggregation": {
                "method": "dynamic",
                "expansion-rate": 1.5,
                "number-bins-per-level": 9}}]}

        self.run_validate(d)

    def test_simulation(self):
        d = {'simulation': {'name': 'Basic GLHE',
                            'initial-temperature': 15,
                            'time-steps-per-hour': 60,
                            'runtime': 3600}}

        self.run_validate(d)

    def test_soil(self):
        d = {'soil': {'name': 'Some Rock',
                      'conductivity': 2.4234,
                      'density': 1500,
                      'specific-heat': 1466}}

        self.run_validate(d)

    def test_validate_temperature_profile(self):
        d = {'temperature-profile': [
            {'temperature-profile-type': 'constant',
             'name': 'constant',
             'value': 1}]}

        self.run_validate(d)

        d = {'temperature-profile': [
            {'temperature-profile-type': 'external',
             'name': 'from ext file',
             'path': 'some/path/to/file'}]}

        self.run_validate(d)

    def test_validate_pipe(self):
        d = {'pipe': [
            {'pipe-def-name': '32 mm SDR-11 HDPE',
             'name': 'my name',
             'length': 100}]}

        self.run_validate(d)

    def test_all_schema_tests_implemented(self):
        # this count should match the number of schema validations implemented here
        # it will match against the count of all schema files in 'glhe/input_processor/schema'
        # not great, but OK for now
        test_count = 14

        fpath = os.path.dirname(os.path.abspath(__file__))
        schema_dir = os.path.normpath(os.path.join(fpath, '..', '..', '..', 'glhe', 'input_processor', 'schema'))
        schema_count = len([name for name in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, name))])
        self.assertEqual(test_count, schema_count)

    def test_file_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: InputProcessor('some path'))

    def test_validate_validation_error(self):
        d = {'soil': {'name': 'Some Rock',
                      'not-a-field': 2.4234,
                      'density': 1500,
                      'specific-heat': 1466}}

        with self.assertRaises(ValidationError) as _:
            InputProcessor.validate_inputs(d)

    def test_get_definition_object_fail(self):
        d = {'pipe': [
            {'pipe-def-name': '32 mm SDR-11 HDPE',
             'name': 'my name',
             'length': 100}]}

        temp_dir = tempfile.mkdtemp()
        f_path = os.path.join(temp_dir, 'temp.json')
        write_json(f_path, d)
        ip = InputProcessor(f_path)
        with self.assertRaises(KeyError) as _:
            ip.get_definition_object('pipe-definitions', 'not-implemented')
