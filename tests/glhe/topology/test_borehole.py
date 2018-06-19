import unittest

from glhe.properties.fluid import Fluid
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
        tst = Borehole(json_blob, {"type": "water", "concentration": 0})
        self.assertEqual(tst._name, json_blob["name"])
        self.assertEqual(tst._depth, json_blob["depth"])
        self.assertEqual(tst._diameter, json_blob["diameter"])
        self.assertEqual(tst._grout.conductivity, json_blob["grout"]["conductivity"])
        self.assertEqual(tst._grout.density, json_blob["grout"]["density"])
        self.assertEqual(tst._grout.specific_heat, json_blob["grout"]["specific heat"])
        self.assertEqual(tst._pipe.specific_heat, json_blob["pipe"]["specific heat"])
        self.assertEqual(tst._pipe.density, json_blob["pipe"]["density"])
        self.assertEqual(tst._pipe.conductivity, json_blob["pipe"]["conductivity"])

    def test_get_flow_resistance(self):
        tst = Borehole(json_blob, Fluid({"type": "water", "concentration": 0}))
        tolerance = 1
        self.assertAlmostEqual(tst.get_flow_resistance(), 115301, delta=tolerance)

    def test_set_flow_rate(self):
        tst = Borehole(json_blob, Fluid({"type": "water", "concentration": 0}))
        tst.set_flow_rate(1)
        tolerance = 0.001
        self.assertAlmostEqual(tst.mass_flow_rate, 1.0, delta=tolerance)
