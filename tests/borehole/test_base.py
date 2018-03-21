import unittest

from glhe.borehole.base import BoreholeBase


class TestBoreholeSimpleHX(unittest.TestCase):

    def test_a(self):
        tst = BoreholeBase(None)
        self.assertEqual(tst.get_outlet_temps(10, 10, 1), None)
