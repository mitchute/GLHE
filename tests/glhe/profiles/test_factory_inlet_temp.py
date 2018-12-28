import os
import tempfile
import unittest

from glhe.profiles.external_inlet_temps import ExternalInletTemps
from glhe.profiles.inlet_temp_factory import make_inlet_temp_profile


class TestFactoryInletTemp(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        temp_data = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_data, 'w') as f:
            f.write('Date/Time, Meas. Total Power [W], mdot [kg/s]\n'
                    '2018-01-01 00:00:00, 1, 1, 1\n'
                    '2018-01-01 01:00:00, 2, 2, 2\n'
                    '2018-01-01 02:00:00, 3, 3, 3\n'
                    '2018-01-01 03:00:00, 4, 4, 4\n')

        return temp_data

    def test_factory_type(self):
        inputs = {'external': {'path': self.add_instance()}}
        profile = make_inlet_temp_profile(inputs=inputs)
        self.assertIsInstance(profile, ExternalInletTemps)

    def test_error(self):
        inputs = {'type': 'bob'}
        self.assertRaises(KeyError, lambda: make_inlet_temp_profile(inputs=inputs))
