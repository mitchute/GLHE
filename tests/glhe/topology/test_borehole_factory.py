import unittest

from glhe.input_processor.component_types import ComponentTypes


class TestBoreholeFactory(unittest.TestCase):

    def test_init_single_u_tube(self):
        tst = ComponentTypes.BoreholeSingleUTube
        self.assertEqual(tst, ComponentTypes.BoreholeSingleUTube)