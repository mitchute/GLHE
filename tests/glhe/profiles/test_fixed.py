import unittest

from glhe.profiles.constant_flow import ConstantFlow


class TestFixed(unittest.TestCase):

    def test_get_value(self):
        tst = ConstantFlow(1)
        self.assertEqual(tst.get_value(), 1)
