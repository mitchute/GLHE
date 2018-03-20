import unittest

from glhe.topology.borehole import Borehole


class TestBorehole(unittest.TestCase):

    def test_a(self):

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

        tst = Borehole(json_blob)
        self.assertEqual(tst._name, json_blob["name"])
        self.assertEqual(tst._depth, json_blob["depth"])
        self.assertEqual(tst._diameter, json_blob["diameter"])
        self.assertEqual(tst._grout._conductivity, json_blob["grout"]["conductivity"])
        self.assertEqual(tst._grout._density, json_blob["grout"]["density"])
        self.assertEqual(tst._grout._specific_heat, json_blob["grout"]["specific heat"])
        self.assertEqual(tst._pipe._specific_heat, json_blob["pipe"]["specific heat"])
        self.assertEqual(tst._pipe._density, json_blob["pipe"]["density"])
        self.assertEqual(tst._pipe._conductivity, json_blob["pipe"]["conductivity"])
