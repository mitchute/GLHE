import unittest

from glhe.topology.segment import Segment
from glhe.topology.segment_types import SegmentType


class TestSegment(unittest.TestCase):

    def test_init(self):
        tst = Segment(segment_type="simple")
        self.assertEqual(tst._type, SegmentType.SIMPLE)
