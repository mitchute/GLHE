import unittest

from glhe.properties.base_properties import PropertiesBase
from glhe.properties.fluid_properties import Fluid
from glhe.properties.props_manager import PropsMGR


class TestPropsMGR(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {
            "fluid": {
                "fluid-type": "water",
                "concentration": 100},
            "soil": {
                "name": "Some Rock",
                "conductivity": 2.6,
                "density": 2500,
                "specific-heat": 880
            }
        }

        props_mgr = PropsMGR()
        props_mgr.load_properties(d)
        return props_mgr

    def test_fluid_instance(self):
        props_mgr = self.add_instance()
        self.assertIsInstance(props_mgr.fluid, Fluid)
        self.assertEqual(props_mgr.fluid.type, 'WATER')

    def test_soil_instance(self):
        props_mgr = self.add_instance()
        self.assertIsInstance(props_mgr.soil, PropertiesBase)
        self.assertEqual(props_mgr.soil.name, 'Some Rock')
