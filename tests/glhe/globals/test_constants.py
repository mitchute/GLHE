import unittest

import glhe.globals.constants as c


class TestConstants(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(c.DAYS_IN_YEAR, 365)
        self.assertEqual(c.HOURS_IN_DAY, 24)
        self.assertEqual(c.MIN_IN_HOUR, 60)
        self.assertEqual(c.SEC_IN_MIN, 60)
        self.assertEqual(c.SEC_IN_HOUR, 60 * 60)
        self.assertEqual(c.SEC_IN_DAY, 60 * 60 * 24)
        self.assertEqual(c.SEC_IN_YEAR, 60 * 60 * 24 * 365)
