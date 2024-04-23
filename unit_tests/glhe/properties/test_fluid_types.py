import unittest

from glhe.properties.fluid_types import FluidType


class TestFluidType(unittest.TestCase):

    def test_init(self):
        tst_w = FluidType.WATER
        self.assertEqual(tst_w, FluidType.WATER)

        tst_ea = FluidType.ETHYL_ALCOHOL
        self.assertEqual(tst_ea, FluidType.ETHYL_ALCOHOL)

        tst_eg = FluidType.ETHYLENE_GLYCOL
        self.assertEqual(tst_eg, FluidType.ETHYLENE_GLYCOL)

        tst_pg = FluidType.PROPYLENE_GLYCOL
        self.assertEqual(tst_pg, FluidType.PROPYLENE_GLYCOL)
