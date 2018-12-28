import unittest

from glhe.topology.segment_types import SegmentType


class TestSegmentType(unittest.TestCase):

    def test_init(self):
        tst = SegmentType.SINGLE_U_TUBE
        self.assertEqual(tst, SegmentType.SINGLE_U_TUBE)
