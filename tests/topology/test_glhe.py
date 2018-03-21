import unittest

from glhe.topology.glhe import GLHE


class TestGLHE(unittest.TestCase):

    def test_init(self):

        json_blob = {"name": "Basic GLHE",
                     "paths": [
                         {"name": "path 1",
                             "boreholes": [
                                 {"name": "borehole 1",
                                  "depth": 50,
                                  "diameter": 0.1524,
                                  "grout": {
                                      "conductivity": 0.75,
                                      "density": 1000,
                                      "specific heat": 1000},
                                  "pipe": {
                                      "outer diameter": 0.0334,
                                      "inner diameter": 0.0269,
                                      "conductivity": 0.4,
                                      "density": 950,
                                      "specific heat": 1000},
                                  "segments": 10,
                                  "type": "simple"}]}],
                     "fluid": {
                         "type": "water",
                         "concentration": 100},
                     "soil": {
                         "conductivity": 2.5,
                         "density": 1500,
                         "specific heat": 1700}}

        tst = GLHE(json_blob)
        self.assertEqual(tst._name, json_blob["name"])
        self.assertEqual(tst.simulate(20, 1, 300), None)
