import unittest

from glhe.properties.pipe import Pipe


class TestPipe(unittest.TestCase):

    def test_init(self):
        tst = Pipe(100, 200, 300)
        self.assertEqual(tst._conductivity, 100)
        self.assertEqual(tst._density, 200)
        self.assertEqual(tst._specific_heat, 300)
