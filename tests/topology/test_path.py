import unittest

from glhe.topology.path import Path


class TestPath(unittest.TestCase):

    def test_a(self):

        json_blob = {"name": "path 1",
                     "boreholes": [
                         {"name": "borehole 1",
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
                          "type": "simple"}]}

        tst = Path(json_blob)
        self.assertEqual(tst._name, json_blob["name"])
        self.assertEqual(len(tst._boreholes), 1)

        tst_bh = tst._boreholes[0]

        self.assertEqual(tst_bh._name, json_blob["boreholes"][0]["name"])
        self.assertEqual(tst_bh._depth, json_blob["boreholes"][0]["depth"])
        self.assertEqual(tst_bh._diameter,
                         json_blob["boreholes"][0]["diameter"])
        self.assertEqual(tst_bh._grout._conductivity,
                         json_blob["boreholes"][0]["grout"]["conductivity"])
        self.assertEqual(tst_bh._grout._density,
                         json_blob["boreholes"][0]["grout"]["density"])
        self.assertEqual(tst_bh._grout._specific_heat,
                         json_blob["boreholes"][0]["grout"]["specific heat"])
        self.assertEqual(tst_bh._pipe._specific_heat,
                         json_blob["boreholes"][0]["pipe"]["specific heat"])
        self.assertEqual(tst_bh._pipe._density,
                         json_blob["boreholes"][0]["pipe"]["density"])
        self.assertEqual(tst_bh._pipe._conductivity,
                         json_blob["boreholes"][0]["pipe"]["conductivity"])
