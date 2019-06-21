import unittest

from glhe.ground_temps.constant import Constant
from glhe.ground_temps.ground_temp_factory import make_ground_temp_model
from glhe.ground_temps.single_harmonic import SingleHarmonic
from glhe.ground_temps.two_harmonic import TwoHarmonic


class TestGTMFactory(unittest.TestCase):
    def test_ground_temperature_model_factory(self):
        inputs = {'ground-temperature-model-type': 'constant',
                  'temperature': 20}

        model = make_ground_temp_model(inputs=inputs)
        self.assertIsInstance(model, Constant)

        inputs = {'ground-temperature-model-type': 'single-harmonic',
                  'soil-diffusivity': 1e-6,
                  'average-temperature': 20,
                  'amplitude': 0,
                  'phase-shift': 0}

        model = make_ground_temp_model(inputs=inputs)
        self.assertIsInstance(model, SingleHarmonic)

        inputs = {'ground-temperature-model-type': 'two-harmonic',
                  'soil-diffusivity': 1e-6,
                  'average-temperature': 20,
                  'amplitude-1': 10,
                  'amplitude-2': 0,
                  'phase-shift-1': 0,
                  'phase-shift-2': 0}

        model = make_ground_temp_model(inputs=inputs)
        self.assertIsInstance(model, TwoHarmonic)

        inputs = {'ground-temperature-model-type': 'bob'}
        self.assertRaises(ValueError, lambda: make_ground_temp_model(inputs=inputs))
