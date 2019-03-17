import unittest

from glhe.g_function.flow_fraction import FlowFraction
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class TestFlowFraction(unittest.TestCase):

    @staticmethod
    def add_instance():
        d_flow_frac = {'BH Depth': 76.2,
                       'BH Radius': 0.057,
                       'Soil Conductivity': 0.85,
                       'Soil Vol Heat Capacity': 2.2E6,
                       'Fluid Vol Heat Capacity': 4.18E6,
                       'Fluid Volume': 0.0568837}

        d_bh = {
            'location': {
                'x': 0,
                'y': 0,
                'z': 1
            },
            'borehole-data': {
                'name': 'borehole type 1',
                'depth': 76.2,
                'diameter': 0.114,
                'initial temp': 20,
                'grout-data': {
                    'name': 'standard grout',
                    'conductivity': 0.85,
                    'density': 1500,
                    'specific heat': 2400
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
                'shank-spacing': 0.0469
            }
        }

        soil_inputs = {'conductivity': 2.6,
                       'density': 1500,
                       'specific heat': 1733}

        fluid = Fluid({'type': 'water'})
        soil = PropertiesBase(soil_inputs)

        return FlowFraction(d_flow_frac), SingleUTubeGroutedBorehole(inputs=d_bh['borehole-data'],
                                                                     fluid_inst=fluid,
                                                                     soil_inst=soil), fluid, soil

    def test_calc_flow_fraction(self):
        tol = 0.001

        tst, bh, fluid, soil = self.add_instance()

        temp = 16
        fluid.update_properties(temp)
        sim_time = 0
        vol_flow_rate = 0.0003
        mass_flow_rate = vol_flow_rate / fluid.density
        bh.set_flow_rate(mass_flow_rate)
        bh_int_resist = bh.calc_bh_total_internal_resistance()
        bh_resist = bh.calc_bh_average_resistance()
        f = tst.calc_flow_fraction(sim_time, vol_flow_rate, bh_int_resist, bh_resist)
        self.assertAlmostEqual(f, 0, delta=tol)

        temp = 16
        fluid.update_properties(temp)
        sim_time = 60
        vol_flow_rate = 0.0003
        mass_flow_rate = vol_flow_rate / fluid.density
        bh.set_flow_rate(mass_flow_rate)
        bh_int_resist = bh.calc_bh_total_internal_resistance()
        bh_resist = bh.calc_bh_average_resistance()
        f = tst.calc_flow_fraction(sim_time, vol_flow_rate, bh_int_resist, bh_resist)
        self.assertAlmostEqual(f, 0.185, delta=tol)

        temp = 16
        fluid.update_properties(temp)
        sim_time = 200
        vol_flow_rate = 0.0003
        mass_flow_rate = vol_flow_rate / fluid.density
        bh.set_flow_rate(mass_flow_rate)
        bh_int_resist = bh.calc_bh_total_internal_resistance()
        bh_resist = bh.calc_bh_average_resistance()
        f = tst.calc_flow_fraction(sim_time, vol_flow_rate, bh_int_resist, bh_resist)
        self.assertAlmostEqual(f, 0.373, delta=tol)

        temp = 16
        fluid.update_properties(temp)
        sim_time = 2000
        vol_flow_rate = 0.0003
        mass_flow_rate = vol_flow_rate / fluid.density
        bh.set_flow_rate(mass_flow_rate)
        bh_int_resist = bh.calc_bh_total_internal_resistance()
        bh_resist = bh.calc_bh_average_resistance()
        f = tst.calc_flow_fraction(sim_time, vol_flow_rate, bh_int_resist, bh_resist)
        self.assertAlmostEqual(f, 0.451, delta=tol)
