import os
import tempfile
import unittest

from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.flow_factory import make_flow_profile


class TestFlowFactory(unittest.TestCase):

    def test_constant_flow(self):
        d = {'flow-profile': [{'flow-profile-type': 'constant', 'name': 'my name', 'value': 1}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        tst = make_flow_profile(d['flow-profile'][0], ip, op)
        self.assertIsInstance(tst, ConstantFlow)

    def test_external_flow(self):
        fpath = os.path.dirname(os.path.abspath(__file__))
        rel_path = '../../../glhe/profiles/external_data/GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv'

        d = {
            'flow-profile':
                [{'flow-profile-type': 'external',
                  'name': 'my name',
                  'path': os.path.join(fpath, rel_path)}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        tst = make_flow_profile(d['flow-profile'][0], ip, op)
        self.assertIsInstance(tst, ExternalFlow)

    def test_fail(self):
        d = {'flow-profile': [{'flow-profile-type': 'constant', 'name': 'my name', 'value': 1}]}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')

        with self.assertRaises(ValueError) as _:
            make_flow_profile({'flow-profile-type': 'not-a-type'}, ip, op)
