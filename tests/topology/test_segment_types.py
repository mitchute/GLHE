import unittest

from glhe.topology.segment_types import SegmentType


class TestSegmentType(unittest.TestCase):

    def test_init(self):
        tst = SegmentType.SIMPLE
        self.assertEqual(tst, SegmentType.SIMPLE)
