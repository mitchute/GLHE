import os
import tempfile
import unittest

from glhe.utilities.interp import Interp2Vars


class TestFunctions(unittest.TestCase):

    @staticmethod
    def add_instance():
        temp_dir = tempfile.mkdtemp()
        f_path = os.path.join(temp_dir, 'temp.csv')
        with open(f_path, 'w') as f:
            f.write('0,5,8\n')
            f.write('1,6,9\n')
            f.write('2,7,10\n')

        return Interp2Vars(f_path, [3, 4])

    def test_init(self):
        tst = self.add_instance()
        self.assertTrue(isinstance(tst, Interp2Vars))

    def test_get_value(self):
        tst = self.add_instance()

        self.assertEqual(tst.get_value(0, 3), 5)
        self.assertEqual(tst.get_value(1, 3), 6)
        self.assertEqual(tst.get_value(2, 3), 7)

        self.assertEqual(tst.get_value(0, 4), 8)
        self.assertEqual(tst.get_value(1, 4), 9)
        self.assertEqual(tst.get_value(2, 4), 10)

        self.assertEqual(tst.get_value(0.5, 3.5), 7)
        self.assertEqual(tst.get_value(1.5, 3.5), 8)
