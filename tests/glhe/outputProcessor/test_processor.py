import os
import tempfile
import unittest

import pandas as pd

from glhe.output_processor.output_processor import OutputProcessor


class DummyClass(object):
    def __init__(self):
        self.foo = 1

    def report_output(self):
        return {"foo": self.foo}


class TestOutputProcessor(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestOutputProcessor, self).__init__(*args, **kwargs)
        self.op = OutputProcessor()
        self.bar = 2

    def report_output(self):
        return {"bar": self.bar}

    def test_collect_output(self):
        d = DummyClass()

        self.op.collect_output([d.report_output(), self.report_output()])

        self.assertEqual(self.op.df['foo'][0], 1)
        self.assertEqual(self.op.df['bar'][0], 2)

    def test_write_to_file(self):
        d = DummyClass()

        self.op.collect_output([d.report_output(), self.report_output()])

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp_data.csv')
        with open(temp_file, 'w') as f:
            f.write('Some, data, here\n')

        self.op.write_to_file(temp_file)

        self.assertTrue(os.path.exists(temp_file))

        df = pd.read_csv(temp_file)

        self.assertEqual(df['foo'].iloc[0], 1)
        self.assertEqual(df['bar'].iloc[0], 2)
