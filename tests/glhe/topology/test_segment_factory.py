# import unittest
#
# from glhe.properties.base_properties import PropertiesBase
# from glhe.properties.fluid_properties import Fluid
# from glhe.topology.segment_factory import make_segment
# from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment
#
#
# class TestSegmentFactory(unittest.TestCase):
#
#     def test_init_single_u_tube_grouted_segment(self):
#         inputs = {'depth': 100,
#                   'diameter': 0.1099,
#                   'grout-data': {'conductivity': 0.744, 'density': 1500, 'name': 'standard grout',
#                                  'specific heat': 800},
#                   'model': 'single',
#                   'name': 'borehole type 1',
#                   'pipe-data': {'conductivity': 0.389, 'density': 950, 'inner diameter': 0.0269,
#                                 'name': '32 mm SDR-11 HDPE', 'outer diameter': 0.0334, 'specific heat': 1900},
#                   'segments': 10,
#                   'shank-spacing': 0.0521,
#                   'initial temp': 20,
#                   'length': 10.0}
#
#         fluid = Fluid(inputs={'type': 'Water'})
#         grout = PropertiesBase(inputs=inputs['grout-data'])
#         soil = PropertiesBase(inputs={'conductivity': 2.0,
#                                       'density': 1000,
#                                       'specific heat': 1000})
#
#         tst = make_segment(inputs=inputs, fluid_inst=fluid, grout_inst=grout, soil_inst=soil)
#         self.assertIsInstance(tst, SingleUTubeGroutedSegment)
#
#     def test_fail(self):
#         inputs = {'model': 'unknown name'}
#         self.assertRaises(ValueError, lambda: make_segment(inputs=inputs))
