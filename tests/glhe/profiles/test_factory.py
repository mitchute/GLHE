import unittest

from glhe.profiles.external import External
from glhe.profiles.factory import make_load_profile
from glhe.profiles.fixed import Fixed
from glhe.profiles.impulse import Impulse
from glhe.profiles.sinusoid import Sinusoid
from glhe.profiles.synthetic import Synthetic


class TestFactory(unittest.TestCase):

    def test_factory_fixed(self):
        inputs = {'type': 'fixed', 'fixed': {'value': 2000}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, Fixed)

    def test_factory_single_impulse(self):
        inputs = {'type': 'single_impulse', 'single_impulse': {'start-time': 2, 'end-time': 3, 'load-value': 4}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, Impulse)

    def test_factory_external(self):
        inputs = {
            'type': 'external',
            'external': {
                'path': "glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv"
            }
        }
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, External)

    def test_factory_sinusoid(self):
        inputs = {'type': 'sinusoid', 'sinusoid': {'amplitude': 2000, 'offset': 2, 'period': 4}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, Sinusoid)

    def test_factory_synthetic(self):
        inputs = {'type': 'synthetic', 'synthetic': {'type': 'symmetric', 'amplitude': 2}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, Synthetic)

    def test_error(self):
        inputs = {'type': 'bob'}
        self.assertRaises(ValueError, lambda: make_load_profile(inputs=inputs))
