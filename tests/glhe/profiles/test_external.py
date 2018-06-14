import unittest

from glhe.profiles.external import External


class TestExternal(unittest.TestCase):

    def test_get_load(self):
        tst = External("glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv")
        self.assertEqual(tst.get_value(0), 0)
        self.assertEqual(tst.get_value(10 * 3600), -4980.600013)
        self.assertEqual(tst.get_value(8759 * 3600), 0)
        self.assertEqual(tst.get_value(8761 * 3600), 0)