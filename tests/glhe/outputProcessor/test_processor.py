import unittest

from glhe.outputProcessor.processor import op


class DummyClass(object):
    def __init__(self):
        self.foo = 1
        op.register_output_variable(self, 'foo', "Foo")


class TestOutputProcessor(unittest.TestCase):

    def test_register_output_variable(self):
        tst = DummyClass()
        test_dict = op.output_vars_data
        self.assertEqual(getattr(*test_dict['Foo']), tst.foo)

    def test_report_output(self):
        DummyClass()
        op.report_output()
        df = op.df
        self.assertEqual(df['Foo'][0], 1)
