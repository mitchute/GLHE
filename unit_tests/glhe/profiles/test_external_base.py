from pathlib import Path
import tempfile
import unittest

from glhe.profiles.external_base import ExternalBase


class TestExternalBase(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = Path(tempfile.mkdtemp())
        temp_csv = temp_dir / 'temp.csv'

        with temp_csv.open('w') as f:
            f.write(',b,c\n1/1/2018 0:00,1,4\n1/1/2018 0:02,2,3\n1/1/2018 0:04,3,6\n')

        return ExternalBase(temp_csv, 0)

    def test_get_value(self):
        tst = self.add_instance()
        self.assertAlmostEqual(tst.get_value(0), 1.0, delta=0.001)
        self.assertAlmostEqual(tst.get_value(60), 1.5, delta=0.001)
        self.assertAlmostEqual(tst.get_value(120), 2.0, delta=0.001)
