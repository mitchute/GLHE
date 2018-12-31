import unittest

from glhe.topology.borehole_types import BoreholeType


class TestBoreholeType(unittest.TestCase):

    def test_init(self):
        tst = BoreholeType.SINGLE_U_TUBE_GROUTED
        self.assertEqual(tst, BoreholeType.SINGLE_U_TUBE_GROUTED)
