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

        # check that the file was written
        self.assertTrue(os.path.exists(tst.write_path))

        # make sure the data comes out right
        df = pd.read_csv(tst.write_path)
        self.assertEqual(df['foo'].iloc[0], 1)
        self.assertEqual(df['bar'].iloc[0], 2)

        # write to an existing file which has to be deleted first
        tst.write_to_file()
        df = pd.read_csv(tst.write_path)
        self.assertEqual(df['foo'].iloc[0], 1)
        self.assertEqual(df['bar'].iloc[0], 2)

    def test_convert_time_to_timestamp(self):
        tst = self.add_instance()
        tst.df = pd.DataFrame({'Elapsed Time [s]': [0, 60, 120], 'Variable': [1, 2, 3]})
        tst.convert_time_to_timestamp()
        self.assertTrue(tst.df.index.name == 'Date/Time')
