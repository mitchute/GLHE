import unittest

from glhe.ground_temps.constant import Constant


class TestConstantGroundTemp(unittest.TestCase):

    def test_constant_ground_temp(self):
        tst = Constant(15)
        self.assertEqual(tst.get_temp(), 15)
