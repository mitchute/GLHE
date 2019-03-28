import unittest

from glhe.properties.fluid_properties import Fluid
from glhe.properties.fluid_types import FluidType


class TestFluid(unittest.TestCase):

    def test_init(self):
        tst_w = Fluid({'fluid-type': 'water'})
        self.assertEqual(tst_w.fluid_enum, FluidType.WATER)
        self.assertEqual(tst_w.fluid_str, 'WATER')

        tst_ea = Fluid({'fluid-type': 'EA', 'concentration': 50})
        self.assertEqual(tst_ea.fluid_enum, FluidType.ETHYL_ALCOHOL)
        self.assertEqual(tst_ea.fluid_str, 'INCOMP::MEA[0.5]')

        tst_eg = Fluid({'fluid-type': 'EG', 'concentration': 50})
        self.assertEqual(tst_eg.fluid_enum, FluidType.ETHYLENE_GLYCOL)
        self.assertEqual(tst_eg.fluid_str, 'INCOMP::MEG[0.5]')

        tst_pg = Fluid({'fluid-type': 'PG', 'concentration': 50})
        self.assertEqual(tst_pg.fluid_enum, FluidType.PROPYLENE_GLYCOL)
        self.assertEqual(tst_pg.fluid_str, 'INCOMP::MPG[0.5]')

        self.assertRaises(ValueError, lambda: Fluid({'fluid-type': 'Not A Fluid', 'concentration': 0}))

    def test_cond(self):
        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-2

        tst = Fluid({'fluid-type': 'water'})
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

        tst = Fluid({'fluid-type': 'water'})
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

        tst = Fluid({'fluid-type': 'water'})
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

        tst = Fluid({'fluid-type': 'water'})
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

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.calc_viscosity(20), 1.002E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(40), 0.653E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(60), 0.467E-3, delta=tolerance)
        self.assertAlmostEqual(tst.calc_viscosity(80), 0.355E-3, delta=tolerance)

    def test_get_k(self):
        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-2

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.get_k(20), 0.598, delta=tolerance)
        self.assertAlmostEqual(tst.get_k(40), 0.631, delta=tolerance)
        self.assertAlmostEqual(tst.get_k(60), 0.654, delta=tolerance)
        self.assertAlmostEqual(tst.get_k(80), 0.670, delta=tolerance)

    def test_get_cp(self):
        """
        Tests fluid specific heat calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 4.0

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.get_cp(20), 4182, delta=tolerance)
        self.assertAlmostEqual(tst.get_cp(40), 4179, delta=tolerance)
        self.assertAlmostEqual(tst.get_cp(60), 4185, delta=tolerance)
        self.assertAlmostEqual(tst.get_cp(80), 4197, delta=tolerance)

    def test_get_rho(self):
        """
        Tests fluid density calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1.0

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.get_rho(20), 998.0, delta=tolerance)
        self.assertAlmostEqual(tst.get_rho(40), 992.1, delta=tolerance)
        self.assertAlmostEqual(tst.get_rho(60), 983.3, delta=tolerance)
        self.assertAlmostEqual(tst.get_rho(80), 971.8, delta=tolerance)

    def test_get_pr(self):
        """
        Tests fluid Prandtl number calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-1

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.get_pr(20), 7.01, delta=tolerance)
        self.assertAlmostEqual(tst.get_pr(40), 4.32, delta=tolerance)
        self.assertAlmostEqual(tst.get_pr(60), 2.99, delta=tolerance)
        self.assertAlmostEqual(tst.get_pr(80), 2.22, delta=tolerance)

    def test_get_mu(self):
        """
        Tests fluid viscosity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        tolerance = 1E-4

        tst = Fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.get_mu(20), 1.002E-3, delta=tolerance)
        self.assertAlmostEqual(tst.get_mu(40), 0.653E-3, delta=tolerance)
        self.assertAlmostEqual(tst.get_mu(60), 0.467E-3, delta=tolerance)
        self.assertAlmostEqual(tst.get_mu(80), 0.355E-3, delta=tolerance)
