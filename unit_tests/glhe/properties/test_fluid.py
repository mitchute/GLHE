import unittest

from scp.ethyl_alcohol import EthylAlcohol
from scp.ethylene_glycol import EthyleneGlycol
from scp.methyl_alcohol import MethylAlcohol
from scp.propylene_glycol import PropyleneGlycol
from scp.water import Water

from glhe.properties.fluid_factory import get_fluid


class TestFluid(unittest.TestCase):

    def test_init(self):
        tst_w = get_fluid({'fluid-type': 'water'})
        self.assertTrue(isinstance(tst_w, Water))

        tst_ea = get_fluid({'fluid-type': 'EA', 'concentration': 50})
        self.assertTrue(isinstance(tst_ea, EthylAlcohol))

        tst_eg = get_fluid({'fluid-type': 'EG', 'concentration': 50})
        self.assertTrue(isinstance(tst_eg, EthyleneGlycol))

        tst_ma = get_fluid({'fluid-type': 'MA', 'concentration': 50})
        self.assertTrue(isinstance(tst_ma, MethylAlcohol))

        tst_pg = get_fluid({'fluid-type': 'PG', 'concentration': 50})
        self.assertTrue(isinstance(tst_pg, PropyleneGlycol))

        self.assertRaises(ValueError, lambda: get_fluid({'fluid-type': 'Not A Fluid', 'concentration': 0}))

    def test_cond(self):
        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        # TODO: convert to fractional error
        tolerance = 1E-2

        tst = get_fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.k(20), 0.598, delta=tolerance)
        self.assertAlmostEqual(tst.k(40), 0.631, delta=tolerance)
        self.assertAlmostEqual(tst.k(60), 0.654, delta=tolerance)
        self.assertAlmostEqual(tst.k(80), 0.670, delta=tolerance)

    def test_cp(self):
        """
        Tests fluid specific heat calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        # TODO: convert to fractional error
        tolerance = 4.0

        tst = get_fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.cp(20), 4182, delta=tolerance)
        self.assertAlmostEqual(tst.cp(40), 4179, delta=tolerance)
        self.assertAlmostEqual(tst.cp(60), 4185, delta=tolerance)
        self.assertAlmostEqual(tst.cp(80), 4197, delta=tolerance)

    def test_dens(self):
        """
        Tests fluid density calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        # TODO: convert to fractional error
        tolerance = 1.0

        tst = get_fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.rho(20), 998.0, delta=tolerance)
        self.assertAlmostEqual(tst.rho(40), 992.1, delta=tolerance)
        self.assertAlmostEqual(tst.rho(60), 983.3, delta=tolerance)
        self.assertAlmostEqual(tst.rho(80), 971.8, delta=tolerance)

    def test_pr(self):
        """
        Tests fluid Prandtl number calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        # TODO: convert to fractional error
        tolerance = 1E-1

        tst = get_fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.pr(20), 7.01, delta=tolerance)
        self.assertAlmostEqual(tst.pr(40), 4.32, delta=tolerance)
        self.assertAlmostEqual(tst.pr(60), 2.99, delta=tolerance)
        self.assertAlmostEqual(tst.pr(80), 2.22, delta=tolerance)

    def test_visc(self):
        """
        Tests fluid viscosity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        # TODO: convert to fractional error
        tolerance = 1E-4

        tst = get_fluid({'fluid-type': 'water'})
        self.assertAlmostEqual(tst.mu(20), 1.002E-3, delta=tolerance)
        self.assertAlmostEqual(tst.mu(40), 0.653E-3, delta=tolerance)
        self.assertAlmostEqual(tst.mu(60), 0.467E-3, delta=tolerance)
        self.assertAlmostEqual(tst.mu(80), 0.355E-3, delta=tolerance)
