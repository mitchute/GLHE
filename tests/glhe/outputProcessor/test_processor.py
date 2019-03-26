import os
import tempfile
import unittest

import pandas as pd

from glhe.output_processor.output_processor import OutputProcessor


class TestOutputProcessor(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        temp_file_name = 'temp.csv'
        return OutputProcessor(temp_dir, temp_file_name)

    def test_collect_output(self):
        tst = self.add_instance()

        d = {'foo': 1,
             'bar': 2}

        tst.collect_output(d)

        self.assertEqual(tst.df['foo'][0], 1)
        self.assertEqual(tst.df['bar'][0], 2)

    def test_write_to_file(self):
        tst = self.add_instance()

        d = {'foo': 1,
             'bar': 2}

        tst.collect_output(d)
        tst.write_to_file()

        self.assertTrue(os.path.exists(tst.write_path))

        df = pd.read_csv(tst.write_path)

        self.assertEqual(df['foo'].iloc[0], 1)
        self.assertEqual(df['bar'].iloc[0], 2)
