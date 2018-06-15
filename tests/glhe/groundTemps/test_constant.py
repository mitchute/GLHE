import unittest

from glhe.groundTemps.constant import Constant


class TestConstantGroundTemp(unittest.TestCase):

    def test_constant_ground_temp(self):
        tst = Constant(15)
        self.assertEqual(tst.get_temp(), 15)
