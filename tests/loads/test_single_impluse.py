import unittest

from loads.loadProfile.single_impulse import SingleImpulse


class TestSingleImpluse(unittest.TestCase):

    def test_init(self):
        tst = SingleImpulse(1, 0, 10)
        self.assertEqual(tst.get_load(0), 1)
        self.assertEqual(tst.get_load(5), 1)
        self.assertEqual(tst.get_load(10), 0)
