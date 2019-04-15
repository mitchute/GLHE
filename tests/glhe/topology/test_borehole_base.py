# import unittest
#
# from glhe.topology.borehole_base import BoreholeBase
#
# inputs = {'depth': 100, 'diameter': 0.15}
#
#
# class TestBorehole(unittest.TestCase):
#
#     @staticmethod
#     def add_instance():
#         return BoreholeBase(inputs=inputs)
#
#     def test_init(self):
#         tst = self.add_instance()
#         self.assertEqual(tst.diameter, inputs['diameter'])
#         self.assertEqual(tst.radius, inputs['diameter'] / 2)
#         self.assertEqual(tst.length, inputs['depth'])
