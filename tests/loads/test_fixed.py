import unittest

from loads.loadProfile.fixed import Fixed


class TestFixed(unittest.TestCase):

    def test_init(self):
        tst = Fixed(1)
        self.assertEqual(tst.get_load(), 1)
