import unittest

from glhe.properties.base import PropertiesBase


class TestBaseProperties(unittest.TestCase):

    def test_init(self):
        b = PropertiesBase({'conductivity': 1, 'density': 2, 'specific heat': 3})
        self.assertEqual(b.conductivity, 1)
        self.assertEqual(b.density, 2)
        self.assertEqual(b.specific_heat, 3)
