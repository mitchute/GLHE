from pathlib import Path
import tempfile
import unittest

from glhe.input_processor.input_processor import InputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.flow_factory import make_flow_profile
from glhe.functions import write_json


class TestFlowFactory(unittest.TestCase):

    def test_constant_flow(self):
        d = {'flow-profile': [{'flow-profile-type': 'constant', 'name': 'my name', 'value': 1}]}

        temp_dir = Path(tempfile.mkdtemp())
        temp_file = temp_dir / 'temp.json'

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)

        tst = make_flow_profile(d['flow-profile'][0], ip)
        self.assertIsInstance(tst, ConstantFlow)

    def test_external_flow(self):
        dir_name = Path(__file__).parent
        root_dir = dir_name.parent.parent.parent
        data_folder = root_dir / 'glhe' / 'profiles' / 'external_data'
        path = data_folder / 'GSHP-GLHE_USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.csv'

        d = {
            'flow-profile':
                [{'flow-profile-type': 'external',
                  'name': 'my name',
                  'path': str(path)}]}

        temp_dir = Path(tempfile.mkdtemp())
        temp_file = temp_dir / 'temp.json'

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)

        tst = make_flow_profile(d['flow-profile'][0], ip)
        self.assertIsInstance(tst, ExternalFlow)

    def test_fail(self):
        d = {'flow-profile': [{'flow-profile-type': 'constant', 'name': 'my name', 'value': 1}]}

        temp_dir = Path(tempfile.mkdtemp())
        temp_file = temp_dir / 'temp.json'

        write_json(temp_file, d)

        ip = InputProcessor(temp_file)

        with self.assertRaises(ValueError) as _:
            make_flow_profile({'flow-profile-type': 'not-a-type'}, ip)
