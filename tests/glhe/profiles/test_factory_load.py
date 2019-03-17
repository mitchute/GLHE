import unittest

from glhe.profiles.external_load import ExternalLoad
from glhe.profiles.load_factory import make_load_profile
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.impulse_load import ImpulseLoad
from glhe.profiles.sinusoid_load import SinusoidLoad
from glhe.profiles.synthetic_load import SyntheticLoad


class TestLoadFactory(unittest.TestCase):

    def test_factory_fixed(self):
        inputs = {'type': 'fixed', 'fixed': {'value': 2000}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, ConstantFlow)

    def test_factory_single_impulse(self):
        inputs = {'type': 'single_impulse', 'single_impulse': {'start-time': 2, 'end-time': 3, 'load-value': 4}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, ImpulseLoad)

    def test_factory_external(self):
        inputs = {
            'type': 'external',
            'external': {
                'path': "glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv"
            }
        }
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, ExternalLoad)

    def test_factory_sinusoid(self):
        inputs = {'type': 'sinusoid', 'sinusoid': {'amplitude': 2000, 'offset': 2, 'period': 4}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, SinusoidLoad)

    def test_factory_synthetic(self):
        inputs = {'type': 'synthetic', 'synthetic': {'type': 'symmetric', 'amplitude': 2}}
        profile = make_load_profile(inputs=inputs)
        self.assertIsInstance(profile, SyntheticLoad)

    def test_error(self):
        inputs = {'type': 'bob'}
        self.assertRaises(ValueError, lambda: make_load_profile(inputs=inputs))
