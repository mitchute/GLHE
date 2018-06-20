import unittest

from glhe.properties.fluid import Fluid
from glhe.topology.borehole import Borehole


class TestBorehole(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {"name": "borehole 1",
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
                  "soil": {
                      "name": "Some Rock",
                      "conductivity": 2.4234,
                      "density": 1500,
                      "specific heat": 1466
                  },
                  "segments": 10,
                  "type": "simple"}

        fluid = Fluid({"type": "water"})

        return Borehole(inputs=inputs, fluid=fluid, soil=inputs["soil"])

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst._name, "borehole 1")
        self.assertEqual(tst._depth, 50)
        self.assertEqual(tst._diameter, 0.1524)
        self.assertEqual(tst._grout.conductivity, 0.75)
        self.assertEqual(tst._grout.density, 1000)
        self.assertEqual(tst._grout.specific_heat, 1000)
        self.assertEqual(tst._pipe.specific_heat, 1000)
        self.assertEqual(tst._pipe.density, 950)
        self.assertEqual(tst._pipe.conductivity, 0.4)

    def test_get_flow_resistance(self):
        tst = self.add_instance()
        tolerance = 1
        self.assertAlmostEqual(tst.get_flow_resistance(), 115301, delta=tolerance)

    def test_set_flow_rate(self):
        tst = self.add_instance()
        tst.set_flow_rate(1)
        tolerance = 0.001
        self.assertAlmostEqual(tst.mass_flow_rate, 1.0, delta=tolerance)
