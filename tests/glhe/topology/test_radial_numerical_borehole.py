import unittest

from math import pi

from glhe.topology.radial_numerical_borehole import RadialCell
from glhe.topology.radial_numerical_borehole import RadialNumericalBH


class TestRadialNumericalBH(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'pipe-outer-diameter': 0.02670,
             'pipe-inner-diameter': 0.02184,
             'diameter': 0.109982,
             'borehole-resistance': 0.2122,
             'convection-resistance': 0.05,
             'fluid-specific-heat': 4180,
             'fluid-density': 998,
             'pipe-specific-heat': 1660,
             'pipe-density': 955,
             'grout-specific-heat': 1000,
             'grout-density': 3900,
             'soil-conductivity': 2.432,
             'soil-specific-heat': 1562,
             'soil-density': 1500,
             'length': 100}

        return RadialNumericalBH(d)

    def test_init(self):

        tst = self.add_instance()

        # type check
        self.assertIsInstance(tst, RadialNumericalBH)

        # type check
        for idx, cell in enumerate(tst.cells):
            self.assertIsInstance(cell, RadialCell)

        # temp check
        for idx, cell in enumerate(tst.cells):
            self.assertEqual(cell.temperature, 20)

        # volume check
        tol = 0.00001
        for idx, cell in enumerate(tst.cells):
            vol = pi * (cell.outer_radius ** 2 - cell.inner_radius ** 2)
            self.assertAlmostEqual(cell.volume, vol, delta=tol)

    def test_calc_sts_g_functions(self):

        tol = 0.01

        tst = self.add_instance()
        lntts, g = tst.calc_sts_g_functions()

        self.assertAlmostEqual(g[0], -2.84, delta=tol)
        self.assertAlmostEqual(g[-1], 2.05, delta=tol)

        self.assertAlmostEqual(lntts[0], -16.00, delta=tol)
        self.assertAlmostEqual(lntts[-1], -9.42, delta=tol)

        tst_2 = self.add_instance()
        lntts_2, g_2 = tst_2.calc_sts_g_functions(calculate_at_bh_wall=True)

        self.assertAlmostEqual(g_2[0], 0.00, delta=tol)
        self.assertAlmostEqual(g_2[-1], 2.05, delta=tol)

        self.assertAlmostEqual(lntts_2[0], -16.00, delta=tol)
        self.assertAlmostEqual(lntts_2[-1], -9.42, delta=tol)
