import unittest

from numpy import log

from glhe.topology.pipe import Pipe
from glhe.properties.fluid import Fluid

json_blob = {"name": "borehole 1",
             "depth": 50,
             "diameter": 0.1524,
             "grout":
                 {"conductivity": 0.75,
                  "density": 1000,
                  "specific heat": 1000},
             "pipe":
                 {"outer diameter": 0.0334,
                  "inner diameter": 0.0269,
                  "conductivity": 0.4,
                  "density": 950,
                  "specific heat": 1000},
             "segments": 10,
             "type": "simple"}


class TestPipe(unittest.TestCase):

    def test_init(self):
        tst = Pipe(1, 2, 3)
        self.assertEqual(tst.conductivity, 1)
        self.assertEqual(tst.density, 2)
        self.assertEqual(tst.specific_heat, 3)

    def test_calc_friction_factor(self):
        """
        Test the smooth tube friction factor calculations
        """

        tst = Pipe(json_blob, Fluid({"type": "water", "concentration": 0}))

        tolerance = 0.00001

        # laminar tests
        re = 100  # noqa: E126
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1000
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1400
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.034003503, delta=tolerance)

        re = 3000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.033446219, delta=tolerance)

        re = 4000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.03895358, delta=tolerance)

        # turbulent tests
        re = 5000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 15000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 25000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))
