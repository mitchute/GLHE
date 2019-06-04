import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.swedish_heat_pump import SwedishHP


class TestSwedishHP(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()

        with open(os.path.join(temp_dir, 'temp.csv'), 'w') as f:
            f.write('Date/Time,Heating Loads (kWh),Water Heating Loads (kWh),Outdoor Air Temperature (C)\n')
            f.write('1/1/2019 0:00,0.751231087,0,4\n')
            f.write('1/1/2019 1:00,0.609682528,0.060515364,5.3\n')
            f.write('1/1/2019 2:00,0.728634445,0.041330207,6.2\n')
            f.write('1/1/2019 3:00,0.562383158,0.042178469,6.8\n')
            f.write('1/1/2019 4:00,0.685067724,0.063096246,7.2\n')
            f.write('1/1/2019 5:00,0.539127476,0.043947185,7.5\n')
            f.write('1/1/2019 6:00,0.663467736,0.044849591,7.5\n')
            f.write('1/1/2019 7:00,0.53908215,0.16588032,6.7\n')
            f.write('1/1/2019 8:00,0.692252428,0.02656684,6\n')
            f.write('1/1/2019 9:00,0.564562993,0.888906269,5.2\n')
            f.write('1/1/2019 10:00,0.670844481,1.230286559,5.2\n')
            f.write('1/1/2019 11:00,0.453722975,0.610134925,5.2\n')
            f.write('1/1/2019 12:00,0.538938447,0.771268588,5.2\n')
            f.write('1/1/2019 13:00,0.460832251,0.030826198,4.6\n')
            f.write('1/1/2019 14:00,0.674925154,0.051852264,4.1\n')
            f.write('1/1/2019 15:00,0.583467315,1.515140121,3.5\n')
            f.write('1/1/2019 16:00,0.769103444,10.85159779,3.2\n')
            f.write('1/1/2019 17:00,0.621861048,10.85240995,2.9\n')
            f.write('1/1/2019 18:00,0.807407677,45,2.6\n')
            f.write('1/1/2019 19:00,0.646501964,1.77903981,2.5\n')
            f.write('1/1/2019 20:00,0.830903352,0.15721722,2.4\n')
            f.write('1/1/2019 21:00,0.661800554,0.358381625,2.3\n')
            f.write('1/1/2019 22:00,0.847617722,0.038695181,2.3\n')
            f.write('1/1/2019 23:00,0.675803234,0.179849569,2.2\n')

        inputs = {'swedish-heat-pump': [{'name': 'svenska varmmepumpe',
                                         'max-heating-set-point': 55,
                                         'min-heating-set-point': 30,
                                         'water-heating-set-point': 60,
                                         'outdoor-air-temperature-at-max-heating-set-point': -10,
                                         'outdoor-air-temperature-at-min-heating-set-point': 20,
                                         'immersion-heater-capacity': 7,
                                         'load-data-path': os.path.join(temp_dir, 'temp.csv'),
                                         'capacity-coefficients': [8.536666667, -0.007266667,
                                                                   -0.00084, 0.263666667],
                                         'coefficient-of-performance-coefficients': [7.641839817, -0.075098454,
                                                                                     -0.000208441, 0.109423218],
                                         }]}

        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, inputs)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return SwedishHP(inputs['swedish-heat-pump'][0], ip, op)

    def test_init(self):
        tst = self.add_instance()
        self.assertIsInstance(tst, SwedishHP)

    def test_set_htg_exft(self):
        tst = self.add_instance()
        tol = 0.001
        # checked against JDS VBA code
        self.assertAlmostEqual(tst.set_htg_exft(0), 43.333, delta=tol)
        self.assertAlmostEqual(tst.set_htg_exft(3600), 42.25, delta=tol)
        self.assertAlmostEqual(tst.set_htg_exft(7200), 41.5, delta=tol)
        self.assertAlmostEqual(tst.set_htg_exft(10800), 41.0, delta=tol)

    def test_x7_cop(self):
        tst = self.add_instance()
        tol = 0.001
        # checked against JDS VBA code
        self.assertAlmostEqual(tst.x7_cop(-10, 60), 1.2913, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(-5, 60), 1.8384, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(0, 60), 2.3855, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(5, 60), 2.9326, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(10, 60), 3.4797, delta=tol)

        self.assertAlmostEqual(tst.x7_cop(-10, 40), 3.2101, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(-5, 40), 3.7572, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(0, 40), 4.3043, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(5, 40), 4.8515, delta=tol)
        self.assertAlmostEqual(tst.x7_cop(10, 40), 5.3986, delta=tol)

    def test_x7_capacity(self):
        tst = self.add_instance()
        tol = 0.01
        # checked against JDS VBA code
        self.assertAlmostEqual(tst.x7_capacity(-10, 60), 2.44, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(-5, 60), 3.76, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(0, 60), 5.08, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(5, 60), 6.39, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(10, 60), 7.71, delta=tol)

        self.assertAlmostEqual(tst.x7_capacity(-10, 40), 4.27, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(-5, 40), 5.58, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(0, 40), 6.90, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(5, 40), 8.22, delta=tol)
        self.assertAlmostEqual(tst.x7_capacity(10, 40), 9.54, delta=tol)

    def test_calc_wtr_htg(self):
        tst = self.add_instance()
        # test case where hp meet load
        tst.calc_wtr_htg(0, 3600, 4)

        # test case where hp and heater meet load
        tst.calc_wtr_htg(3600 * 16, 3600, 4)

        # test case where some loads are unmet
        tst.calc_wtr_htg(3600 * 18, 3600, 4)

    def test_calc_htg(self):
        tst = self.add_instance()
        # test case where hp meet load
        tst.calc_htg(0, 3600, 4)

        # test case where hp and heater meet load
        tst.calc_htg(3600 * 16, 3600, 4)

        # test case where some loads are unmet
        tst.calc_htg(3600 * 18, 3600, 4)
