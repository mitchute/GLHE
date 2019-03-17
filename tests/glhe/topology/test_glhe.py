# import os
# import tempfile
# import unittest
#
# from glhe.globals.functions import write_json
# from glhe.input_processor.input_processor import InputProcessor
# from glhe.topology.full_ground_loop import GLHE
#
#
# class TestGLHE(unittest.TestCase):
#
#     @staticmethod
#     def add_instance():
#         d = {
#             "borehole-definitions": [
#                 {
#                     "name": "borehole type 1",
#                     "depth": 100,
#                     "diameter": 0.1099,
#                     "grout-type": "standard grout",
#                     "model": "single",
#                     "pipe-type": "32 mm SDR-11 HDPE",
#                     "segments": 10,
#                     "shank-spacing": 0.0521
#                 }
#             ],
#             "flow-profile": {
#                 "type": "fixed",
#                 "fixed": {
#                     "value": 1
#                 },
#                 "external": {
#                     "path": "./glhe/profiles/external_data"
#                 }
#             },
#             "fluid": {
#                 "type": "water",
#                 "concentration": 100
#             },
#             "g-functions": {
#                 "file": "../glhe/examples/2x2_g_functions.csv",
#                 "average-depth": 100,
#                 "borehole-type": "borehole type 1"
#             },
#             "ground-temperature": {
#                 "type": "constant",
#                 "constant": {
#                     "temperature": 20
#                 },
#                 "single-harmonic": {
#                     "ave-temperature": 20,
#                     "amplitude": 0,
#                     "phase-shift": 0
#                 },
#                 "two-harmonic": {
#                     "ave-temperature": 20,
#                     "amplitude-1": 10,
#                     "amplitude-2": 0,
#                     "phase-shift-1": 0,
#                     "phase-shift-2": 0
#                 }
#             },
#             "grout-definitions": [
#                 {
#                     "name": "standard grout",
#                     "conductivity": 0.744,
#                     "density": 1500,
#                     "specific heat": 800
#                 }
#             ],
#             "load-aggregation": {
#                 "type": "dynamic",
#                 "dynamic": {
#                     "param 1": 1
#                 }
#             },
#             "load-profile": {
#                 "type": "fixed",
#                 "fixed": {
#                     "value": 2000
#                 },
#                 "single-impulse": {
#                     "start-time": 100,
#                     "end-time": 200,
#                     "value": 3000
#                 },
#                 "external": {
#                     "path": "./glhe/profiles/external_data"
#                 },
#                 "sinusoid": {
#                     "amplitude": 1000,
#                     "offset": 0,
#                     "period": 0
#                 },
#                 "synthetic": {
#                     "type": "symmetric",
#                     "amplitude": 1000
#                 }
#             },
#             "paths": [
#                 {
#                     "name": "path 1",
#                     "boreholes": [
#                         {
#                             "name": "borehole 1",
#                             "location": {
#                                 "x": 0,
#                                 "y": 0,
#                                 "z": 1
#                             },
#                             "borehole-type": "borehole type 1"
#                         },
#                         {
#                             "name": "borehole 2",
#                             "location": {
#                                 "x": 1,
#                                 "y": 0,
#                                 "z": 1
#                             },
#                             "borehole-type": "borehole type 1"
#                         }
#                     ]
#                 },
#                 {
#                     "name": "path 2",
#                     "boreholes": [
#                         {
#                             "name": "borehole 3",
#                             "location": {
#                                 "x": 0,
#                                 "y": 1,
#                                 "z": 1
#                             },
#                             "borehole-type": "borehole type 1"
#                         },
#                         {
#                             "name": "borehole 4",
#                             "location": {
#                                 "x": 1,
#                                 "y": 1,
#                                 "z": 1
#                             },
#                             "borehole-type": "borehole type 1"
#                         }
#                     ]
#                 }
#             ],
#             "pipe-definitions": [
#                 {
#                     "name": "32 mm SDR-11 HDPE",
#                     "outer diameter": 0.0334,
#                     "inner diameter": 0.0269,
#                     "conductivity": 0.389,
#                     "density": 950,
#                     "specific heat": 1900
#                 }
#             ],
#             "simulation": {
#                 "name": "Basic GLHE",
#                 "time-step": 3600,
#                 "runtime": 31536000
#             },
#             "soil": {
#                 "name": "Some Rock",
#                 "conductivity": 2.4234,
#                 "density": 1500,
#                 "specific heat": 1466
#             }
#         }
#
#         temp_dir = tempfile.mkdtemp()
#         temp_file = os.path.join(temp_dir, 'temp.json')
#
#         write_json(temp_file, d)
#
#         inputs = InputProcessor().process_input(temp_file)
#         return GLHE(inputs=inputs)
#
#     def test_init(self):
#         tst = self.add_instance()
#
#         tst.set_flow_rates(1)
#         self.assertAlmostEqual(tst.delta_p_path, 115402, delta=1)
#
#     def test_flow_distribution(self):
#         tst = self.add_instance()
#         tst.set_flow_rates(1)
#         self.assertAlmostEqual(tst.paths[0].mass_flow_rate, 0.5, delta=0.01)
#         self.assertAlmostEqual(tst.paths[1].mass_flow_rate, 0.5, delta=0.01)
