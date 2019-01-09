import unittest

from glhe.gFunction.calc_sts_g_functions import STSGFunctions
from glhe.gFunction.radial_sts_cell import RadialCell
from glhe.globals.constants import PI
from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


class TestSTSGFunctions(unittest.TestCase):

    @staticmethod
    def add_instance():

        bh_inputs = {
            'name': 'borehole type 1',
            'depth': 100,
            'diameter': 0.109982,
            'initial temp': 20,
            'grout-data': {
                'name': 'standard grout',
                'conductivity': 0.744,
                'density': 3900,
                'specific heat': 1000
            },
            'model': 'single',
            'pipe-data': {
                'name': '32 mm SDR-11 HDPE',
                'outer diameter': 0.0267,
                'inner diameter': 0.02184,
                'conductivity': 0.389,
                'density': 1770,
                'specific heat': 1000
            },
            'segments': 10,
            'shank-spacing': 0.04566
        }

        soil_inputs = {'conductivity': 2.423,
                       'density': 1500,
                       'specific heat': 1562}

        fluid = Fluid({'type': 'water'})
        soil = PropertiesBase(soil_inputs)

        bh = SingleUTubeGroutedBorehole(inputs=bh_inputs, fluid_inst=fluid, soil_inst=soil)

        rho_f = fluid.calc_density(20)
        cp_f = fluid.calc_specific_heat(20)

        v_dot = 0.00018927
        m_dot = v_dot * rho_f

        bh.set_flow_rate(m_dot)

        bh_resist = bh.calc_bh_average_resistance()
        conv_resist = bh.pipe.calc_convection_resistance(m_dot)

        inputs = {'borehole diameter': bh_inputs['diameter'],
                  'borehole resistance': bh_resist,
                  'convection resistance': conv_resist,
                  'soil conductivity': soil_inputs['conductivity'],
                  'soil density': soil_inputs['density'],
                  'soil specific heat': soil_inputs['specific heat'],
                  'initial temperature': 20,
                  'pipe outer diameter': bh_inputs['pipe-data']['outer diameter'],
                  'pipe inner diameter': bh_inputs['pipe-data']['inner diameter'],
                  'pipe density': bh_inputs['pipe-data']['density'],
                  'pipe specific heat': bh_inputs['pipe-data']['specific heat'],
                  'grout density': bh_inputs['grout-data']['density'],
                  'grout specific heat': bh_inputs['grout-data']['specific heat'],
                  'fluid density': rho_f,
                  'fluid specific heat': cp_f
                  }

        return STSGFunctions(inputs)

    def test_init(self):

        tst = self.add_instance()

        # type check
        self.assertIsInstance(tst, STSGFunctions)

        # type check
        for idx, cell in enumerate(tst.cells):
            self.assertIsInstance(cell, RadialCell)

        # type check
        for idx, cell in enumerate(tst.cells):
            self.assertIsInstance(cell, RadialCell)

        # temp check
        for idx, cell in enumerate(tst.cells):
            self.assertEqual(cell.temperature, 20)

        # volume check
        tol = 0.00001
        for idx, cell in enumerate(tst.cells):
            vol = PI * (cell.outer_radius ** 2 - cell.inner_radius ** 2)
            self.assertAlmostEquals(cell.volume, vol, delta=tol)

    def test_calc_sts_g_functions(self):

        tst = self.add_instance()
        tst.calc_sts_g_functions()
        pass
