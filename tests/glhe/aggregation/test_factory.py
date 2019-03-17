import unittest

from glhe.aggregation.dynamic_method import DynamicMethod
from glhe.aggregation.aggregation_factory import load_agg_factory
from glhe.aggregation.no_aggregation_method import NoAggMethod
from glhe.aggregation.static_method import StaticMethod


class TestFactory(unittest.TestCase):

    def test_static(self):
        inputs = {'type': 'static'}
        agg_method = load_agg_factory(inputs=inputs)
        self.assertIsInstance(agg_method, StaticMethod)

    def test_dynamic(self):
        inputs = {'type': 'dynamic'}
        agg_method = load_agg_factory(inputs=inputs)
        self.assertIsInstance(agg_method, DynamicMethod)

    def test_no_aggregation(self):
        inputs = {'type': 'none'}
        agg_method = load_agg_factory(inputs=inputs)
        self.assertIsInstance(agg_method, NoAggMethod)

    def test_error(self):
        inputs = {'type': 'bob'}
        self.assertRaises(ValueError, lambda: load_agg_factory(inputs=inputs))
