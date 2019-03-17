import unittest

from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.constant_flow import ConstantFlow


class TestFlowFactory(unittest.TestCase):

    def test_factory_fixed(self):
        inputs = {'type': 'fixed', 'fixed': {'value': 1}}
        profile = make_flow_profile(inputs=inputs)
        self.assertIsInstance(profile, ConstantFlow)

    def test_factory_external(self):
        inputs = {
            'type': 'external',
            'external': {
                'path': "glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv"
            }
        }
        profile = make_flow_profile(inputs=inputs)
        self.assertIsInstance(profile, ExternalFlow)

    def test_error(self):
        inputs = {'type': 'bob'}
        self.assertRaises(ValueError, lambda: make_flow_profile(inputs=inputs))
