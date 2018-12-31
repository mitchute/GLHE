import unittest

from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.single_u_tube_borehole import SingleUTubeBorehole


class TestBorehole(unittest.TestCase):

    @staticmethod
    def add_instance(my_inputs=None):
        if my_inputs is None:
            my_inputs = {'radius': 0.048,
                         'shank-spacing': 0.032,
                         'soil conductivity': 4.0,
                         'grout conductivity': 0.6}

        inputs = {
            'location': {
                'x': 0,
                'y': 0,
                'z': 1
            },
            'borehole-data': {
                'name': 'borehole type 1',
                'depth': 76.2,
                'diameter': my_inputs['radius'] * 2,
                'initial temp': 20,
                'grout-data': {
                    'name': 'standard grout',
                    'conductivity': my_inputs['grout conductivity'],
                    'density': 1000,
                    'specific heat': 1000
                },
                'model': 'single',
                'pipe-data': {
                    'name': '32 mm SDR-11 HDPE',
                    'outer diameter': 0.032,
                    'inner diameter': 0.02714,
                    'conductivity': 0.389,
                    'density': 800,
                    'specific heat': 1000
                },
                'segments': 10,
                'shank-spacing': my_inputs['shank-spacing']
            }
        }

        soil_inputs = {'conductivity': my_inputs['soil conductivity'],
                       'density': 1500,
                       'specific heat': 1663.8}

        fluid = Fluid({'type': 'water'})
        soil = PropertiesBase(soil_inputs)

        return SingleUTubeBorehole(inputs=inputs['borehole-data'], fluid=fluid, soil=soil)

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst.DEPTH, 76.2)
        self.assertEqual(tst.DIAMETER, 0.096)
        self.assertEqual(tst.grout.conductivity, 0.6)
        self.assertEqual(tst.grout.density, 1000)
        self.assertEqual(tst.grout.specific_heat, 1000)
        self.assertEqual(tst.pipe.specific_heat, 1000)
        self.assertEqual(tst.pipe.density, 800)
        self.assertEqual(tst.pipe.conductivity, 0.389)

    def test_get_flow_resistance(self):
        tst = self.add_instance()
        tolerance = 1
        self.assertAlmostEqual(tst.get_flow_resistance(), 168086, delta=tolerance)

    def test_set_flow_rate(self):
        tst = self.add_instance()
        tst.set_flow_rate(1)
        tolerance = 0.001
        self.assertAlmostEqual(tst.mass_flow_rate, 1.0, delta=tolerance)

    def test_calc_bh_total_internal_resistance(self):
        tolerance = 0.00001

        inputs = {}
        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.32365, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23126, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.19830, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18070, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16947, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16152, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.32754, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23529, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20214, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18428, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16453, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.33415, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24161, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20788, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18942, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17734, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16864, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34783, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25298, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21738, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.19744, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18420, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17456, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.45329, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29701, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24310, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21511, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.19766, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18555, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.46560, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.30669, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25113, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.22197, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20363, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.19082, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.48651, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.32190, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26312, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23184, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21196, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.19800, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.52992, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34923, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.28294, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24724, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.22443, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20837, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.44849, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.33093, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.28097, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25194, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23252, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21839, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.49081, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35908, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.30227, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26911, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24689, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23075, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.56145, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.40275, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.33381, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29370, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26696, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24762, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.70364, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.47982, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.38537, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.33186, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29691, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.27207, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35072, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24556, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20667, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18552, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17194, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16235, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35151, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24649, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20760, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18641, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16310, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35289, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24797, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20901, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18769, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17390, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16412, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35595, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25077, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21141, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18971, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17561, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16558, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.79250, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.46254, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35062, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29359, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25871, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23502, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.80334, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.47089, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35730, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29907, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26330, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.23893, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.82235, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.48435, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.36744, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.30702, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26973, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24425, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.86441, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.50970, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.38466, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.31960, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.27937, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25189, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.61186, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.46146, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.39174, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34857, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.31835, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29565, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.68753, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.51388, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.43140, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.38012, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34428, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.31748, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.81754, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.59704, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.49099, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.42563, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.38053, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34722, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 1.09392, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.74945, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.59065, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.49705, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.43476, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.39009, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35512, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24806, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20819, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18641, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17239, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16250, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35546, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24847, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20860, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18680, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16284, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35606, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.24912, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.20922, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18737, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17326, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16329, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35739, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.25036, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.21029, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.18827, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.17402, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.16394, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.99531, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.56245, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.41627, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34215, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.29705, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.26657, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 1.00551, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.57026, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.42245, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.34718, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.30122, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.27010, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 1.02350, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.58289, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.43187, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.35448, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.30706, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.27488, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 1.06368, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.60688, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.44794, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.36606, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.31582, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.28175, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.68527, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.52300, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.44557, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.39656, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.36169, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.33518, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.77817, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.58840, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.49530, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.43614, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.39417, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.36245, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.93884, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.69271, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.57029, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.49335, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.43958, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.39955, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 1.28480, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.88570, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.69643, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.58336, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.50757, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_total_internal_resistance(), 0.45299, delta=tolerance)

    def test_calc_bh_grout_resistance(self):
        tolerance = 0.00001

        inputs = {}
        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.17701, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09211, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06329, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04861, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03965, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03358, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.17732, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09230, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06341, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04869, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03970, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03361, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.17787, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09259, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06358, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04880, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03977, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03366, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.17910, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09315, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06387, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04897, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03988, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03373, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.14218, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07445, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05122, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03931, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03200, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02704, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.14295, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07492, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05153, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03952, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03216, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02716, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.14429, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07567, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05199, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03983, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03237, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02732, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.14724, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07707, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05278, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04032, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03270, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.04266667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02754, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06695, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04131, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03069, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02461, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02061, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.01776, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07090, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04361, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03222, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02572, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02146, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.01844, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07759, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04720, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03450, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02731, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02265, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.01936, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09138, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05361, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03825, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02979, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02442, delta=tolerance)

        inputs['radius'] = 0.048
        inputs['shank-spacing'] = 0.06400000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02069, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.36382, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.18488, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12489, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09471, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07647, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.36384, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.18489, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12490, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09471, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07647, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.36387, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.18491, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12491, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09472, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07648, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.36394, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.18494, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12493, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09473, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07649, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.26405, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.13316, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08934, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06733, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05407, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04520, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.26434, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.13336, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08948, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06744, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05416, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04527, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.26484, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.13369, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08971, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06760, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05428, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04537, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.26597, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.13430, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09009, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06786, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05447, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.07466667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04551, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09055, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05854, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04486, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03684, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03146, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02757, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09914, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06410, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04889, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03995, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03397, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.02964, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.11380, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07288, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05492, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04444, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03747, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03247, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.14454, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08878, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06494, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05145, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04270, delta=tolerance)

        inputs['radius'] = 0.096
        inputs['shank-spacing'] = 0.16000000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03656, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.47152, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.23870, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09798, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.47153, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.23870, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.47153, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.23871, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.47155, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.23871, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16077, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.03200000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.32711, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16421, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.10980, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08254, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06615, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05521, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.32731, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16436, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.10991, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08263, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06623, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05527, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.32768, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16460, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.11009, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08276, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06633, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05535, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.32850, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.16507, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.11038, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08297, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06648, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.10666667
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05547, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.10481, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06997, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05467, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04553, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03930, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 4.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03472, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.11665, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.07790, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06054, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05011, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04302, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 3.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.03782, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.13696, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.09047, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06934, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05672, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04821, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 2.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04204, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 0.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.18002, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.2
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.11344, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 1.8
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.08403, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 2.4
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.06709, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.0
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.05599, delta=tolerance)

        inputs['radius'] = 0.144
        inputs['shank-spacing'] = 0.25600000
        inputs['soil conductivity'] = 1.0
        inputs['grout conductivity'] = 3.6
        tst = self.add_instance(my_inputs=inputs)
        tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(tst.calc_bh_grout_resistance(), 0.04812, delta=tolerance)

    def test_calc_bh_resistance(self):
        tolerance = 0.00001
        tst = self.add_instance()
        tst.set_flow_rate(0.5)
        self.assertAlmostEqual(tst.calc_bh_effective_resistance(), 0.21629, delta=tolerance)
