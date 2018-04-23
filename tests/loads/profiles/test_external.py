import unittest

from loads.profiles.external import External


class TestExternal(unittest.TestCase):

    def test_get_load(self):
        tst = External("loads/profiles/external/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv")
        self.assertEqual(tst.get_load(0), 0)
        self.assertEqual(tst.get_load(10 * 3600), -4980.600013)
        self.assertEqual(tst.get_load(8759 * 3600), 0)
        self.assertEqual(tst.get_load(8761 * 3600), 0)
