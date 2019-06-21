import unittest

from glhe.ground_temps.constant import Constant


class TestConstantGroundTemp(unittest.TestCase):

    def test_constant_ground_temp(self):
        inputs = {'temperature': 15}
        tst = Constant(inputs)
        self.assertEqual(tst.get_temp(), 15)
