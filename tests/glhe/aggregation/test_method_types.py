import unittest

from glhe.aggregation.method_types import MethodType


class TestMethodType(unittest.TestCase):

    def test_init(self):
        tst_dynamic = MethodType.DYNAMIC
        self.assertEqual(tst_dynamic, MethodType.DYNAMIC)

        tst_static = MethodType.STATIC
        self.assertEqual(tst_static, MethodType.STATIC)

        tst_no_agg = MethodType.NOAGG
        self.assertEqual(tst_no_agg, MethodType.NOAGG)
