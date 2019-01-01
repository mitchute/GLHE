import unittest

from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.segment_factory import make_segment

inputs = {'depth': 100,
          'diameter': 0.1099,
          'grout-data': {'conductivity': 0.744, 'density': 1500, 'name': 'standard grout',
                         'specific heat': 2.6},
          'model': 'single',
          'name': 'borehole type 1',
          'pipe-data': {'conductivity': 0.389, 'density': 950, 'inner diameter': 0.0269,
                        'name': '32 mm SDR-11 HDPE', 'outer diameter': 0.0334, 'specific heat': 1.623},
          'segments': 10,
          'shank-spacing': 0.0521,
          'initial temp': 20,
          'length': 10.0}


class TestSingleUTubeGroutedSegment(unittest.TestCase):

    @staticmethod
    def add_instance():
        fluid = Fluid(inputs={'type': 'Water'})
        grout = PropertiesBase(inputs=inputs['grout-data'])
        soil = PropertiesBase(inputs={'conductivity': 2.0,
                                      'density': 1000,
                                      'specific heat': 1000})

        return make_segment(inputs=inputs, fluid_inst=fluid, grout_inst=grout, soil_inst=soil)

    def test_init(self):
        tst = self.add_instance()
        tol = 0.0001

        self.assertAlmostEqual(tst.DIAMETER, inputs['diameter'], delta=tol)
        self.assertAlmostEqual(tst.LENGTH, inputs['length'], delta=tol)

        self.assertAlmostEqual(tst.TOTAL_VOL, 9.4860E-2, delta=tol)
        self.assertAlmostEqual(tst.PIPE_VOL, 6.1567E-3, delta=tol)
        self.assertAlmostEqual(tst.FLUID_VOL, 1.1366E-2, delta=tol)
        self.assertAlmostEqual(tst.GROUT_VOL, 9.4860E-2 - 1.1366E-2 - 6.1567E-3, delta=tol)
