import unittest

from glhe.properties.fluid import Fluid
from glhe.topology.path import Path


class TestPath(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {"name": "path 1",
                  "boreholes": [
                      {"name": "borehole 1",
                       "depth": 50,
                       "diameter": 0.1524,
                       "shank-spacing": 0.0521,
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
                       "type": "simple"}],
                  "soil": {
                      "conductivity": 2.5,
                      "density": 1500,
                      "specific heat": 1700}
                  }

        fluid = Fluid({"type": "water"})

        return Path(inputs, fluid, soil=inputs["soil"])

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst._name, "path 1")
        self.assertEqual(len(tst._boreholes), 1)

        tst_bh = tst._boreholes[0]

        self.assertEqual(tst_bh._name, "borehole 1")
        self.assertEqual(tst_bh._depth, 50)
        self.assertEqual(tst_bh._diameter, 0.1524)
        self.assertEqual(tst_bh._grout.conductivity, 0.75)
        self.assertEqual(tst_bh._grout.density, 1000)
        self.assertEqual(tst_bh._grout.specific_heat, 1000)
        self.assertEqual(tst_bh._pipe.specific_heat, 1000)
        self.assertEqual(tst_bh._pipe.density, 950)
        self.assertEqual(tst_bh._pipe.conductivity, 0.4)
