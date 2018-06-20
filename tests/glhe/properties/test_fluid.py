import unittest

from glhe.properties.fluid import Fluid
from glhe.properties.fluid_types import FluidType


class TestFluid(unittest.TestCase):

    def test_init(self):
        tst_w = Fluid({"type": "water", "concentration": 0})
        self.assertEqual(tst_w._type, FluidType.WATER)
        self.assertEqual(tst_w._min_temperature, 0)
        self.assertEqual(tst_w._max_temperature, 200)
        self.assertEqual(tst_w._fluid_str, "WATER")

        tst_ea = Fluid({"type": "EA", "concentration": 50})
        self.assertEqual(tst_ea._type, FluidType.ETHYL_ALCOHOL)
        self.assertEqual(tst_ea._min_temperature, -100)
        self.assertEqual(tst_ea._max_temperature, 40)
        self.assertEqual(tst_ea._min_concentration, 0)
        self.assertEqual(tst_ea._max_concentration, 60)
        self.assertEqual(tst_ea._fluid_str, "INCOMP::MEA[0.5]")

        tst_eg = Fluid({"type": "EG", "concentration": 50})
        self.assertEqual(tst_eg._type, FluidType.ETHYLENE_GLYCOL)
        self.assertEqual(tst_eg._min_temperature, -100)
        self.assertEqual(tst_eg._max_temperature, 100)
        self.assertEqual(tst_eg._min_concentration, 0)
        self.assertEqual(tst_eg._max_concentration, 60)
        self.assertEqual(tst_eg._fluid_str, "INCOMP::MEG[0.5]")

        tst_pg = Fluid({"type": "PG", "concentration": 50})
        self.assertEqual(tst_pg._type, FluidType.PROPYLENE_GLYCOL)
        self.assertEqual(tst_pg._min_temperature, -100)
        self.assertEqual(tst_pg._max_temperature, 100)
        self.assertEqual(tst_pg._min_concentration, 0)
        self.assertEqual(tst_pg._max_concentration, 60)
        self.assertEqual(tst_pg._fluid_str, "INCOMP::MPG[0.5]")

        self.assertRaises(ValueError, lambda: Fluid({"type": "Not A Fluid", "concentration": 0}))

    def test_cond(self):
        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-2

        tst = Fluid({"type": "water", "concentration": 0})
        self.assertAlmostEqual(tst.calc_conductivity(20), 0.598, delta=tolerance)
        self.assertAlmostEqual(tst.calc_conductivity(40), 0.631, delta=tolerance)
        self.assertAlmostEqual(tst.calc_conductivity(60), 0.654, delta=tolerance)
        self.assertAlmostEqual(tst.calc_conductivity(80), 0.670, delta=tolerance)

    def test_cp(self):
        """
        Tests fluid specific heat calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 4.0

        tst = Fluid({"type": "water", "concentration": 0})
        self.assertAlmostEqual(tst.calc_specific_heat(20), 4182, delta=tolerance)
        self.assertAlmostEqual(tst.calc_specific_heat(40), 4179, delta=tolerance)
        self.assertAlmostEqual(tst.calc_specific_heat(60), 4185, delta=tolerance)
        self.assertAlmostEqual(tst.calc_specific_heat(80), 4197, delta=tolerance)

    def test_dens(self):
        """
        Tests fluid density calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1.0

        tst = Fluid({"type": "water", "concentration": 0})
        self.assertAlmostEqual(tst.calc_density(20), 998.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_density(40), 992.1, delta=tolerance)
        self.assertAlmostEqual(tst.calc_density(60), 983.3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_density(80), 971.8, delta=tolerance)

    def test_pr(self):
        """
        Tests fluid Prandtl number calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-1

        tst = Fluid({"type": "water", "concentration": 0})
        self.assertAlmostEqual(tst.calc_prandtl(20), 7.01, delta=tolerance)
        self.assertAlmostEqual(tst.calc_prandtl(40), 4.32, delta=tolerance)
        self.assertAlmostEqual(tst.calc_prandtl(60), 2.99, delta=tolerance)
        self.assertAlmostEqual(tst.calc_prandtl(80), 2.22, delta=tolerance)

    def test_visc(self):
        """
        Tests fluid viscosity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-4

        tst = Fluid({"type": "water", "concentration": 0})
        self.assertAlmostEqual(tst.calc_viscosity(20), 1.002E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(40), 0.653E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(60), 0.467E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(80), 0.355E-3, delta=tolerance)
