from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import unittest

import pandas as pd

from glhe.output_processor.output_processor import OutputProcessor


class TestOutputProcessor(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = Path(tempfile.mkdtemp())
        temp_file_name = 'temp.csv'
        return OutputProcessor(temp_dir, temp_file_name)

    def test_collect_output(self):
        tst = self.add_instance()

        d = {'foo': 1,
             'bar': 2}

        tst.collect_output(d)

        self.assertEqual(tst.output_data[0]['foo'], 1)
        self.assertEqual(tst.output_data[0]['bar'], 2)

    def test_write_to_file(self):
        tst = self.add_instance()

        d = {'Elapsed Time [s]': 60, 'foo': 1, 'bar': 2}

        tst.collect_output(d)
        tst.write_to_file()

        # check that the file was written
        self.assertTrue(tst.write_path.exists())

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
        tst.output_data = [
            {'Elapsed Time [s]': 0, 'Variable': 1},
            {'Elapsed Time [s]': 60, 'Variable': 2},
            {'Elapsed Time [s]': 120, 'Variable': 3},
        ]
        time_stamps = tst.convert_time_to_timestamp()
        date_times = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in time_stamps]
        self.assertEqual(date_times[1] - date_times[0], timedelta(minutes=1))
