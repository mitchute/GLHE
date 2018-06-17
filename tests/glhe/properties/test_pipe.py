import unittest

from glhe.properties.pipe import Pipe


class TestPipe(unittest.TestCase):

    def test_init(self):
        tst = Pipe(100, 200, 300)
        self.assertEqual(tst.conductivity, 100)
        self.assertEqual(tst.density, 200)
        self.assertEqual(tst.specific_heat, 300)
