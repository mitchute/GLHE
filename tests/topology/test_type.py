import unittest

from glhe.topology.type import SegmentType


class TestSegmentType(unittest.TestCase):

    def test_a(self):
        tst = SegmentType.SIMPLE
        self.assertEqual(tst, SegmentType.SIMPLE)
