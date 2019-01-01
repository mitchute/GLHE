import unittest

from numpy import log

from glhe.properties.fluid import Fluid
from glhe.topology.pipe import Pipe


class TestPipe(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {
            'outer diameter': 0.0334,
            'inner diameter': 0.0269,
            'conductivity': 0.389,
            'density': 950,
            'specific heat': 1.623,
            'length': 100,
            'initial temp': 20
        }

        fluid = Fluid({'type': 'water'})

        return Pipe(inputs=inputs, fluid_inst=fluid)

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst.conductivity, 0.389)
        self.assertEqual(tst.density, 950)
        self.assertEqual(tst.specific_heat, 1.623)

    def test_calc_friction_factor(self):
        tst = self.add_instance()
        tolerance = 0.00001

        # laminar tests
        re = 100  # noqa: E126
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1000
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1400
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.034003503, delta=tolerance)

        re = 3000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.033446219, delta=tolerance)

        re = 4000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.03895358, delta=tolerance)

        # turbulent tests
        re = 5000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 15000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

        re = 25000
        self.assertEqual(tst.calc_friction_factor(re), (0.79 * log(re) - 1.64) ** (-2.0))

    def test_calc_conduction_resistance(self):
        tst = self.add_instance()
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_conduction_resistance(), 0.088549, delta=tolerance)

    def test_calc_convection_resistance(self):
        tst = self.add_instance()
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_convection_resistance(0), 0.13273, delta=tolerance)
        self.assertAlmostEqual(tst.calc_convection_resistance(0.07), 0.02645, delta=tolerance)
        self.assertAlmostEqual(tst.calc_convection_resistance(2), 0.00094, delta=tolerance)

    def test_calc_resistance(self):
        tst = self.add_instance()
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_resistance(0), 0.22128, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resistance(0.07), 0.11500, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resistance(2), 0.08948, delta=tolerance)

    def test_set_resistance(self):
        tst = self.add_instance()
        tst.set_resistance(1)
        self.assertEqual(tst.resist_pipe, 1)

    def test_calc_outlet_temp_hanby(self):
        tst = self.add_instance()
        tol = 0.05
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 20.0, delta=tol)
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 20.0, delta=tol)
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 20.0, delta=tol)
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 20.4, delta=tol)
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 22.3, delta=tol)
        self.assertAlmostEqual(tst.calc_outlet_temp_hanby(25, 0.0002, 60), 25.0, delta=tol)
