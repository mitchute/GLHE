import unittest

from glhe.gFunction.calc_sts_g_functions import STSGFunctions
from glhe.gFunction.radial_sts_cell import RadialCell
from glhe.globals.constants import PI


class TestSTSGFunctions(unittest.TestCase):

    def add_instance(self):

        inputs = {'borehole radius': 0.1,
                  'soil conductivity': 1.5,
                  'soil density': 1500,
                  'soil specific heat': 1000,
                  'soil temperature': 20}

        return STSGFunctions(inputs)

    def test_init(self):

        tst = self.add_instance()

        # type check
        self.assertIsInstance(tst, STSGFunctions)

        # type check
        for idx, cell in enumerate(tst.cells):
            self.assertIsInstance(cell, RadialCell)

        # type check
        for idx, cell in enumerate(tst.cells):
            self.assertIsInstance(cell, RadialCell)

        # temp check
        for idx, cell in enumerate(tst.cells):
            self.assertEquals(cell.temperature, 20)

        # properties check
        for idx, cell in enumerate(tst.cells):
            self.assertEquals(cell.conductivity, 1.5)
            self.assertEquals(cell.density, 1500)
            self.assertEquals(cell.specific_heat, 1000)

        # volume check
        tol = 0.00001
        for idx, cell in enumerate(tst.cells):
            vol = PI * (cell.radius_outer ** 2 - cell.radius_inner ** 2)
            self.assertAlmostEquals(cell.volume, vol, delta=tol)
