import unittest

from loads.profiles.external import External


class TestExternal(unittest.TestCase):

    def test_init(self):
        tst = External("loads/profiles/external/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv")
        pass
