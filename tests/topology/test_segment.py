import unittest

from glhe.topology.segment import Segment
from glhe.topology.type import SegmentType


class TestSegment(unittest.TestCase):

    def test_a(self):
        tst = Segment(segment_type="simple")
        self.assertEqual(tst._type, SegmentType.SIMPLE)
