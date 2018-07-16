import unittest

from glhe.outputProcessor.processor import OutputProcessor


class DummyClass(object):
    def __init__(self):
        self.foo = 1
        OutputProcessor().register_output_variable(self, 'foo', "Foo")


class TestOutputProcessor(unittest.TestCase):

    def test_register_output_variable(self):
        tst = DummyClass()
        test_dict = OutputProcessor().output_vars_data
        self.assertEqual(getattr(*test_dict['Foo']), tst.foo)

    def test_report_output(self):
        DummyClass()
        OutputProcessor().report_output()
        df = OutputProcessor().df
        self.assertEqual(df['Foo'][0], 1)
