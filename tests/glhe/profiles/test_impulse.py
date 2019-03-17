import unittest

from glhe.profiles.impulse_load import ImpulseLoad


class TestImpulse(unittest.TestCase):

    def test_get_value(self):
        tst = ImpulseLoad(1, 0, 10)
        self.assertEqual(tst.get_value(0), 1)
        self.assertEqual(tst.get_value(5), 1)
        self.assertEqual(tst.get_value(10), 0)
