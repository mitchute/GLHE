import unittest

from glhe.properties.fluid import Fluid
from glhe.topology.segment import Segment
from glhe.topology.segment_types import SegmentType


class TestSegment(unittest.TestCase):

    def test_init(self):
        tst = Segment(model_type="simple", fluid=Fluid({"type": "water", "concentration": 0}))
        self.assertEqual(tst.type, SegmentType.SIMPLE)
