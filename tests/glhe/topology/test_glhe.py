import unittest

from glhe.topology.full_ground_loop import GLHE


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

        tst.set_flow_rates(1)
        self.assertAlmostEqual(tst._delta_p_path, 115402, delta=1)

    def test_flow_distribution(self):
        json_blob = {"name": "Basic GLHE",
                     "paths": [
                         {
                             "name": "path 1",
                             "boreholes": [
                                 {
                                     "name": "borehole 1",
                                     "depth": 50,
                                     "diameter": 0.1524,
                                     "grout":
                                         {
                                             "conductivity": 0.75,
                                             "density": 1000,
                                             "specific heat": 1000
                                         },
                                     "pipe":
                                         {
                                             "outer diameter": 0.0334,
                                             "inner diameter": 0.0269,
                                             "conductivity": 0.4,
                                             "density": 950,
                                             "specific heat": 1000
                                         },
                                     "segments": 10,
                                     "type": "simple"
                                 }
                             ]
                         },
                         {
                             "name": "path 2",
                             "boreholes": [
                                 {
                                     "name": "borehole 2",
                                     "depth": 50,
                                     "diameter": 0.1524,
                                     "grout":
                                         {
                                             "conductivity": 0.75,
                                             "density": 1000,
                                             "specific heat": 1000
                                         },
                                     "pipe":
                                         {
                                             "outer diameter": 0.0334,
                                             "inner diameter": 0.0269,
                                             "conductivity": 0.4,
                                             "density": 950,
                                             "specific heat": 1000
                                         },
                                     "segments": 10,
                                     "type": "simple"
                                 }
                             ]
                         }
                     ],
                     "fluid":
                         {
                             "type": "water",
                             "concentration": 100
                         },
                     "soil":
                         {
                             "conductivity": 2.5,
                             "density": 1500,
                             "specific heat": 1700
                         }
                     }

        tst = GLHE(json_blob)
        tst.set_flow_rates(1)
        self.assertAlmostEqual(tst._paths[0].mass_flow_rate, 0.5, delta=0.01)
        self.assertAlmostEqual(tst._paths[1].mass_flow_rate, 0.5, delta=0.01)
