import unittest

from loads.profiles.single_impulse import SingleImpulse


class TestSingleImpulse(unittest.TestCase):

    def test_get_load(self):
        tst = SingleImpulse(1, 0, 10)
        self.assertEqual(tst.get_load(0), 1)
        self.assertEqual(tst.get_load(5), 1)
        self.assertEqual(tst.get_load(10), 0)
