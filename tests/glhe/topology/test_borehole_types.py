import unittest

from glhe.topology.borehole_types import BoreholeTypes


class TestBoreholeType(unittest.TestCase):

    def test_init(self):
        tst = BoreholeTypes.SINGLE_U_TUBE_GROUTED
        self.assertEqual(tst, BoreholeTypes.SINGLE_U_TUBE_GROUTED)
