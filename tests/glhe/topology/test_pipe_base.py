import unittest

from glhe.topology.pipe_base import PipeBase

inputs = {
    'outer diameter': 0.04,
    'inner diameter': 0.03,
    'conductivity': 0.4,
    'density': 900,
    'specific heat': 2.0,
    'length': 100,
    'initial temp': 20
}


class TestPipe(unittest.TestCase):

    @staticmethod
    def add_instance():
        return PipeBase(inputs=inputs)

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst.INNER_DIAMETER, 0.03)
        self.assertEqual(tst.OUTER_DIAMETER, 0.04)
        self.assertEqual(tst.conductivity, 0.4)
        self.assertEqual(tst.density, 900)
        self.assertEqual(tst.specific_heat, 2.0)
        self.assertEqual(tst.LENGTH, 100)

    def test_geometry(self):
        tst = self.add_instance()
        tol_1 = 0.000001
        tol_2 = 0.01

        self.assertAlmostEqual(tst.THICKNESS, 0.005, delta=tol_1)
        self.assertAlmostEqual(tst.INNER_RADIUS, 0.015, delta=tol_1)
        self.assertAlmostEqual(tst.OUTER_RADIUS, 0.02, delta=tol_1)

        self.assertAlmostEqual(tst.AREA_CR_INNER, 7.0685E-4, delta=tol_1)
        self.assertAlmostEqual(tst.AREA_CR_OUTER, 1.2566E-3, delta=tol_1)
        self.assertAlmostEqual(tst.AREA_CR_PIPE, 1.2566E-3 - 7.0685E-4, delta=tol_1)

        self.assertAlmostEqual(tst.AREA_S_INNER, 9.4247, delta=tol_2)
        self.assertAlmostEqual(tst.AREA_S_OUTER, 12.566, delta=tol_2)

        self.assertAlmostEqual(tst.TOTAL_VOL, 1.2566E-1, delta=tol_2)
        self.assertAlmostEqual(tst.FLUID_VOL, 7.0685E-2, delta=tol_2)
        self.assertAlmostEqual(tst.PIPE_WALL_VOL, 1.2566E-1 - 7.0685E-2, delta=tol_2)
