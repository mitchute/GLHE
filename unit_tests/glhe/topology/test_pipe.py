import os
import tempfile
import unittest
from math import log

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.pipe import Pipe
from glhe.utilities.functions import write_json


class TestPipe(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {'pipe-definitions': [{
            'name': '32 mm sdr-11 hdpe',
            'outer-diameter': 0.0334,
            'inner-diameter': 0.0269,
            'conductivity': 0.4,
            'density': 950,
            'specific-heat': 1900}],
            'fluid': {'fluid-type': 'water'},
            'pipe': [
                {'pipe-def-name': '32 mm sdr-11 hdpe',
                 'name': 'pipe 1',
                 'length': 100}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')
        write_json(temp_file, inputs)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        return Pipe(inputs['pipe'][0], ip, op)

    def test_init(self):
        tst = self.add_instance()
        tol = 0.0001

        # props
        self.assertAlmostEqual(tst.conductivity, 0.4, delta=tol)
        self.assertAlmostEqual(tst.density, 950, delta=tol)
        self.assertAlmostEqual(tst.specific_heat, 1900, delta=tol)
        self.assertAlmostEqual(tst.heat_capacity, 950 * 1900, delta=tol)
        self.assertAlmostEqual(tst.diffusivity, 0.4 / (950 * 1900), delta=tol)

        # geometry
        self.assertAlmostEqual(tst.outer_diameter, 0.0334, delta=tol)
        self.assertAlmostEqual(tst.inner_diameter, 0.0269, delta=tol)
        self.assertAlmostEqual(tst.length, 100, delta=tol)
        self.assertAlmostEqual(tst.outer_radius, 0.0334 / 2, delta=tol)
        self.assertAlmostEqual(tst.inner_radius, 0.0269 / 2, delta=tol)
        self.assertAlmostEqual(tst.wall_thickness, 0.00325, delta=tol)

        # areas
        self.assertAlmostEqual(tst.area_cr_outer, 8.761E-4, delta=tol)
        self.assertAlmostEqual(tst.area_cr_inner, 5.628E-4, delta=tol)
        self.assertAlmostEqual(tst.area_cr_pipe, 3.078E-4, delta=tol)
        self.assertAlmostEqual(tst.area_s_outer, 10.4929, delta=tol)
        self.assertAlmostEqual(tst.area_s_inner, 8.4508, delta=tol)

        # volumes
        self.assertAlmostEqual(tst.total_vol, 0.0876, delta=tol)
        self.assertAlmostEqual(tst.fluid_vol, 0.0568, delta=tol)
        self.assertAlmostEqual(tst.pipe_wall_vol, 0.0307, delta=tol)

    def test_calc_friction_factor(self):
        tst = self.add_instance()
        tol = 0.00001

        # laminar tests
        re = 100  # noqa: E126
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1000
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        re = 1400
        self.assertEqual(tst.calc_friction_factor(re), 64.0 / re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.034003503, delta=tol)

        re = 3000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.033446219, delta=tol)

        re = 4000
        self.assertAlmostEqual(tst.calc_friction_factor(re), 0.03895358, delta=tol)

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
        self.assertAlmostEqual(tst.calc_cond_resist(), 0.0861146, delta=tolerance)

    def test_calc_convection_resistance(self):
        tst = self.add_instance()
        temp = 20
        tol = 0.00001
        self.assertAlmostEqual(tst.calc_conv_resist(0, temp), 0.13273, delta=tol)
        self.assertAlmostEqual(tst.calc_conv_resist(0.07, temp), 0.02645, delta=tol)
        self.assertAlmostEqual(tst.calc_conv_resist(2, temp), 0.00094, delta=tol)

    def test_calc_resistance(self):
        tst = self.add_instance()
        temp = 20
        tolerance = 0.00001
        self.assertAlmostEqual(tst.calc_resist(0, temp), 0.218852, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resist(0.07, temp), 0.11256, delta=tolerance)
        self.assertAlmostEqual(tst.calc_resist(2, temp), 0.08704, delta=tolerance)

    def test_calc_transit_time(self):
        tst = self.add_instance()
        tol = 0.1
        self.assertAlmostEqual(tst.calc_transit_time(0.1, 20), 567.3, delta=tol)

    def test_laminar_nusselt(self):
        tst = self.add_instance()
        tol = 0.01
        self.assertAlmostEqual(tst.laminar_nusselt(), 4.01, delta=tol)

    def test_turbulent_nusselt(self):
        tst = self.add_instance()
        tol = 0.01
        self.assertAlmostEqual(tst.turbulent_nusselt(3000, 20), 18.39, delta=tol)
        self.assertAlmostEqual(tst.turbulent_nusselt(10000, 20), 79.52, delta=tol)

    def test_log_inlet_temps(self):
        tst = self.add_instance()
        self.assertEqual(tst.inlet_temps[0], 20)
        self.assertEqual(tst.inlet_temps_times[0], 0)

        self.assertEqual(len(tst.inlet_temps), 1)
        self.assertEqual(len(tst.inlet_temps_times), 1)

        tst.log_inlet_temps(25, 100)

        self.assertEqual(tst.inlet_temps[1], 25)
        self.assertEqual(tst.inlet_temps_times[1], 100)

        self.assertEqual(len(tst.inlet_temps), 2)
        self.assertEqual(len(tst.inlet_temps_times), 2)

    def test_mdot_to_re(self):
        tst = self.add_instance()
        tol = 0.1
        self.assertAlmostEqual(tst.m_dot_to_re(0.1, 20), 4725.7, delta=tol)

    def test_simulate_time_step(self):
        tst = self.add_instance()
        tol = 0.01

        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(0, 100, 0.1, 25)).temperature,
                               20, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(100, 100, 0.1, 25)).temperature,
                               20, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(200, 100, 0.1, 25)).temperature,
                               20, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(300, 100, 0.1, 25)).temperature,
                               20, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(400, 100, 0.1, 25)).temperature,
                               20, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(500, 100, 0.1, 25)).temperature,
                               22.63, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(600, 100, 0.1, 25)).temperature,
                               24.34, delta=tol)
        self.assertAlmostEqual(tst.simulate_time_step(SimulationResponse(700, 100, 0.1, 25)).temperature,
                               24.87, delta=tol)
