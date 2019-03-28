import unittest

from glhe.properties.base_properties import PropertiesBase
from glhe.properties.fluid_properties import Fluid
from glhe.topology.segment_factory import make_segment

inputs = {'depth': 100,
          'diameter': 0.1099,
          'grout-data': {'conductivity': 0.744, 'density': 1500, 'name': 'standard grout',
                         'specific heat': 800},
          'model': 'single',
          'name': 'borehole type 1',
          'pipe-data': {'conductivity': 0.389, 'density': 950, 'inner diameter': 0.0269,
                        'name': '32 mm SDR-11 HDPE', 'outer diameter': 0.0334, 'specific heat': 1900},
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

    def test_simulate(self):
        tst = self.add_instance()
        kwargs = {'borehole wall temp': 20,
                  'inlet 1 temp': 30,
                  'inlet 2 temp': 25,
                  'mass flow rate': 0.2,
                  'borehole resistance': 0.16,
                  'direct coupling resistance': 2.28}

        ret_temps = tst.simulate(1, **kwargs)

        tol = 0.0001
        self.assertAlmostEqual(ret_temps[0], 20.3458, delta=tol)
        self.assertAlmostEqual(ret_temps[1], 20.1729, delta=tol)
        self.assertAlmostEqual(ret_temps[2], 20.0001, delta=tol)
        self.assertAlmostEqual(ret_temps[3], 20.0001, delta=tol)
