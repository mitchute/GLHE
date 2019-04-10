# import os
# import unittest
#
# from standalone.plant_loop import PlantLoop
#
#
# class TestPlantLoop(unittest.TestCase):
#
#     def setUp(self):
#         self.this_file_directory = os.path.dirname(os.path.realpath(__file__))
#
#     def test_simulate(self):
#         json_file_path = os.path.normpath(
#                 os.path.join(self.this_file_directory, '..', '..', 'glhe', 'examples', 'single.json'))
#         p = PlantLoop(json_file_path)
#         self.assertTrue(p.simulate())
