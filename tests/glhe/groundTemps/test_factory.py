import unittest

from glhe.groundTemps.constant import Constant
from glhe.groundTemps.factory import make_ground_temperature_model
from glhe.groundTemps.single_harmonic import SingleHarmonic
from glhe.groundTemps.two_harmonic import TwoHarmonic


class TestGTMFactory(unittest.TestCase):
    def test_make_ground_temperature_model(self):
        inputs = {"type": "constant",
                  "temperature": 20}
        model = make_ground_temperature_model(inputs=inputs)
        self.assertIsInstance(model, Constant)

        inputs = {"type": "single-harmonic",
                  "ave-temperature": 20,
                  "amplitude": 0,
                  "phase-shift": 0,
                  "soil-diffusivity": 1e-6}
        model = make_ground_temperature_model(inputs=inputs)
        self.assertIsInstance(model, SingleHarmonic)

        inputs = {"type": "two-harmonic",
                  "ave-temperature": 20,
                  "amplitude-1": 10,
                  "amplitude-2": 0,
                  "phase-shift-1": 0,
                  "phase-shift-2": 0,
                  "soil-diffusivity": 1e-6}
        model = make_ground_temperature_model(inputs=inputs)
        self.assertIsInstance(model, TwoHarmonic)
