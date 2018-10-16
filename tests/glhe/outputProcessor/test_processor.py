import unittest

from glhe.outputProcessor.processor import OutputProcessor


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

    def test_report_output(self):
        d = DummyClass()

        self.op.collect_output([d.report_output(), self.report_output()])

        self.assertEqual(self.op.df['foo'][0], 1)
        self.assertEqual(self.op.df['bar'][0], 2)
