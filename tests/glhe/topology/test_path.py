import unittest

from glhe.properties.base import PropertiesBase
from glhe.properties.fluid import Fluid
from glhe.topology.path import Path


class TestPath(unittest.TestCase):

    @staticmethod
    def add_instance():
        inputs = {
            'name': 'path 1',
            'boreholes': [
                {
                    'name': 'borehole 1',
                    'location': {
                        'x': 0,
                        'y': 0,
                        'z': 1
                    },
                    'borehole-data': {
                        'name': 'borehole type 1',
                        'depth': 100,
                        'diameter': 0.1099,
                        'grout-data': {
                            'name': 'standard grout',
                            'conductivity': 0.744,
                            'density': 1500,
                            'specific heat': 2.6
                        },
                        'model': 'simple',
                        'pipe-data': {
                            'name': '32 mm SDR-11 HDPE',
                            'outer diameter': 0.0334,
                            'inner diameter': 0.0269,
                            'conductivity': 0.389,
                            'density': 950,
                            'specific heat': 1.623
                        },
                        'segments': 10,
                        'shank-spacing': 0.0521
                    }
                }
            ]
        }

        fluid = Fluid({'type': 'water'})
        soil = PropertiesBase({'conductivity': 2.4234, 'density': 1500, 'specific heat': 1466})

        return Path(inputs, fluid, soil=soil)

    def test_init(self):
        tst = self.add_instance()
        self.assertEqual(tst._name, 'path 1')
        self.assertEqual(len(tst._boreholes), 1)

        tst_bh = tst._boreholes[0]

        self.assertEqual(tst_bh.DEPTH, 100)
        self.assertEqual(tst_bh.DIAMETER, 0.1099)
        self.assertEqual(tst_bh.grout.conductivity, 0.744)
        self.assertEqual(tst_bh.grout.density, 1500)
        self.assertEqual(tst_bh.grout.specific_heat, 2.6)
        self.assertEqual(tst_bh.pipe.specific_heat, 1.623)
        self.assertEqual(tst_bh.pipe.density, 950)
        self.assertEqual(tst_bh.pipe.conductivity, 0.389)
