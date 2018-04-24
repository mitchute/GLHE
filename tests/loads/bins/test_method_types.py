import unittest

from loads.bins.method_types import MethodType


class TestMethodType(unittest.TestCase):

    def test_init(self):
        tst_DYN = MethodType.DYNAMIC
        self.assertEqual(tst_DYN, MethodType.DYNAMIC)

        tst_ST = MethodType.STATIC
        self.assertEqual(tst_ST, MethodType.STATIC)

        tst_NA = MethodType.NOAGG
        self.assertEqual(tst_NA, MethodType.NOAGG)
