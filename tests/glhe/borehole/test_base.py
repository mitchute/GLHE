import unittest

from glhe.borehole.base import BoreholeBase
from glhe.borehole.simpleHX import BoreholeSimpleHX


class TestBoreholeSimpleHX(unittest.TestCase):

    def test_abstract_instantiation_fails(self):
        with self.assertRaises(Exception):
            BoreholeBase(None)

    def test_get_outlet_temps(self):
        tst = BoreholeSimpleHX(None)
        self.assertEqual(tst.get_outlet_temps(10, 10, 1), (10, 10))
