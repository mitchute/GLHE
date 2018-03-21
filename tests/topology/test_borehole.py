import unittest

import numpy as np

from glhe.topology.borehole import Borehole

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


class TestBorehole(unittest.TestCase):

    def test_init(self):

        tst = Borehole(json_blob)
        self.assertEqual(tst._name, json_blob["name"])
        self.assertEqual(tst._depth, json_blob["depth"])
        self.assertEqual(tst._diameter, json_blob["diameter"])
        self.assertEqual(tst._grout._conductivity,
                         json_blob["grout"]["conductivity"])
        self.assertEqual(tst._grout._density, json_blob["grout"]["density"])
        self.assertEqual(tst._grout._specific_heat,
                         json_blob["grout"]["specific heat"])
        self.assertEqual(tst._pipe._specific_heat,
                         json_blob["pipe"]["specific heat"])
        self.assertEqual(tst._pipe._density, json_blob["pipe"]["density"])
        self.assertEqual(tst._pipe._conductivity,
                         json_blob["pipe"]["conductivity"])

    def test_friction_factor(self):
        """
        Test the smooth tube friction factor calculations
        """

        tst = Borehole(json_blob)

        tolerance = 0.00001

        # laminar tests
        re = 100
        self.assertEqual(tst.friction_factor(re), 64.0 / re)

        re = 1000
        self.assertEqual(tst.friction_factor(re), 64.0 / re)

        re = 1400
        self.assertEqual(tst.friction_factor(re), 64.0 / re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(tst.friction_factor(re), 0.034003503, delta=tolerance)

        re = 3000
        self.assertAlmostEqual(tst.friction_factor(re), 0.033446219, delta=tolerance)

        re = 4000
        self.assertAlmostEqual(tst.friction_factor(re), 0.03895358, delta=tolerance)

        # turbulent tests
        re = 5000
        self.assertEqual(tst.friction_factor(re), (0.79 * np.log(re) - 1.64) ** (-2.0))

        re = 15000
        self.assertEqual(tst.friction_factor(re), (0.79 * np.log(re) - 1.64) ** (-2.0))

        re = 25000
        self.assertEqual(tst.friction_factor(re), (0.79 * np.log(re) - 1.64) ** (-2.0))
