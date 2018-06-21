import unittest

from glhe.properties.fluid_types import FluidType


class TestFluidType(unittest.TestCase):

    def test_init(self):
        tst_W = FluidType.WATER
        self.assertEqual(tst_W, FluidType.WATER)

        tst_EA = FluidType.ETHYL_ALCOHOL
        self.assertEqual(tst_EA, FluidType.ETHYL_ALCOHOL)

        tst_EG = FluidType.ETHYLENE_GLYCOL
        self.assertEqual(tst_EG, FluidType.ETHYLENE_GLYCOL)

        tst_PG = FluidType.PROPYLENE_GLYCOL
        self.assertEqual(tst_PG, FluidType.PROPYLENE_GLYCOL)
