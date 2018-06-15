import unittest

from glhe.profiles.fixed import Fixed


class TestFixed(unittest.TestCase):

    def test_get_value(self):
        tst = Fixed(1)
        self.assertEqual(tst.get_value(), 1)
