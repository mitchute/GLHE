import os
import tempfile
import unittest

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.swedish_heat_pump import SwedishHP
from glhe.utilities.functions import w_to_kw
from glhe.utilities.functions import write_json


class TestSwedishHP(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()

        with open(os.path.join(temp_dir, 'temp.csv'), 'w') as f:
            f.write('Date/Time,Heating Loads (W),Water Heating Loads (W),Outdoor Air Temperature (C)\n')
            f.write('1/1/2019 0:00,751.231087,0,4\n')
            f.write('1/1/2019 1:00,609.682528,60.515364,5.3\n')
            f.write('1/1/2019 2:00,728.634445,41.330207,6.2\n')
            f.write('1/1/2019 3:00,562.383158,42.178469,6.8\n')
            f.write('1/1/2019 4:00,685.067724,63.096246,7.2\n')
            f.write('1/1/2019 5:00,539.127476,43.947185,7.5\n')
            f.write('1/1/2019 6:00,663.467736,44.849591,7.5\n')
            f.write('1/1/2019 7:00,539.08215,165.88032,6.7\n')
            f.write('1/1/2019 8:00,692.252428,26.56684,6\n')
            f.write('1/1/2019 9:00,564.562993,888.906269,5.2\n')
            f.write('1/1/2019 10:00,670.844481,1230.286559,5.2\n')
            f.write('1/1/2019 11:00,453.722975,610.134925,5.2\n')
            f.write('1/1/2019 12:00,538.938447,771.268588,5.2\n')
            f.write('1/1/2019 13:00,460.832251,30.826198,4.6\n')
            f.write('1/1/2019 14:00,674.925154,51.852264,4.1\n')
            f.write('1/1/2019 15:00,583.467315,1515.140121,3.5\n')
            f.write('1/1/2019 16:00,769.103444,10851.59779,3.2\n')
            f.write('1/1/2019 17:00,621.861048,10852.40995,2.9\n')
            f.write('1/1/2019 18:00,807.407677,45000,2.6\n')
            f.write('1/1/2019 19:00,646.501964,1779.03981,2.5\n')
            f.write('1/1/2019 20:00,830.903352,157.21722,2.4\n')
            f.write('1/1/2019 21:00,661.800554,358.381625,2.3\n')
            f.write('1/1/2019 22:00,847.617722,38.695181,2.3\n')
            f.write('1/1/2019 23:00,675.803234,179.849569,2.2\n')

        inputs = {'fluid': {'fluid-type': 'PG', 'concentration': 35},
                  'swedish-heat-pump': [{'name': 'svenska varmmepumpe',
                                         'max-heating-set-point': 55,
                                         'min-heating-set-point': 30,
                                         'water-heating-set-point': 60,
                                         'outdoor-air-temperature-at-max-heating-set-point': -10,
                                         'outdoor-air-temperature-at-min-heating-set-point': 20,
                                         'immersion-heater-capacity': 7000,
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
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(-10, 60)), 2.44, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(-5, 60)), 3.76, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(0, 60)), 5.08, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(5, 60)), 6.39, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(10, 60)), 7.71, delta=tol)

        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(-10, 40)), 4.27, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(-5, 40)), 5.58, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(0, 40)), 6.90, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(5, 40)), 8.22, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.x7_capacity(10, 40)), 9.54, delta=tol)

    def test_calc_wtr_htg(self):
        tst = self.add_instance()
        tol = 0.01

        # test case where hp meets load
        tst.calc_wtr_htg(0, 4)
        self.assertAlmostEqual(tst.wtr_htg_elec, 0, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_rtf, 0, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_imm_elec, 0, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_unmet, 0, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_heat_extraction, 0, delta=tol)

        # test case where hp and heater meet load
        tst.calc_wtr_htg(3600 * 16, 4)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_elec), 2.17, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_rtf, 1, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_imm_elec), 4.72, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_unmet), 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_heat_extraction), 3.95, delta=tol)

        # test case where some loads are unmet
        tst.calc_wtr_htg(3600 * 18, 4)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_elec), 2.17, delta=tol)
        self.assertAlmostEqual(tst.wtr_htg_rtf, 1, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_imm_elec), 7, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_unmet), 31.87, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.wtr_htg_heat_extraction), 3.95, delta=tol)

    def test_calc_htg(self):
        tst = self.add_instance()
        tol = 0.01

        # test case where hp meets load
        tst.calc_wtr_htg(0, 4)
        tst.calc_htg(0, 4)
        self.assertAlmostEqual(w_to_kw(tst.htg_elec), 0.17, delta=tol)
        self.assertAlmostEqual(tst.htg_rtf, 0.12, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_imm_elec), 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_unmet), 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_heat_extraction), 0.58, delta=tol)

        # test case where hp and heater meet load
        tst.calc_wtr_htg(3600 * 16, 4)
        tst.calc_htg(3600 * 16, 4)
        self.assertAlmostEqual(w_to_kw(tst.htg_elec), 0, delta=tol)
        self.assertAlmostEqual(tst.htg_rtf, 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_imm_elec), 0.77, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_unmet), 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_heat_extraction), 0, delta=tol)

        # test case where some loads are unmet
        tst.calc_wtr_htg(3600 * 18, 4)
        tst.calc_htg(3600 * 18, 4)
        self.assertAlmostEqual(w_to_kw(tst.htg_elec), 0, delta=tol)
        self.assertAlmostEqual(tst.htg_rtf, 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_imm_elec), 0, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_unmet), 0.81, delta=tol)
        self.assertAlmostEqual(w_to_kw(tst.htg_heat_extraction), 0, delta=tol)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        tol = 0.01

        response = SimulationResponse(0, 3600, 0.3, 20)
        response = tst.simulate_time_step(response)
        self.assertAlmostEqual(response.temperature, 19.44, delta=tol)

        response = SimulationResponse(3600 * 16, 3600, 0.3, 20)
        response = tst.simulate_time_step(response)
        self.assertAlmostEqual(response.temperature, 12.87, delta=tol)

        response = SimulationResponse(3600 * 18, 3600, 0.3, 20)
        response = tst.simulate_time_step(response)
        self.assertAlmostEqual(response.temperature, 12.87, delta=tol)
