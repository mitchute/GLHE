import unittest

from loads.bins.static_method import StaticMethod


class TestStatic(unittest.TestCase):

    def test_init(self):
        tst = StaticMethod(min_bin_nums=[1], bin_widths=[1])
        self.assertEqual(len(tst.loads), 0)

    def test_add_load(self):
        tst = StaticMethod(min_bin_nums=[2, 2, 2], bin_widths=[1, 2, 4])
        tst.add_load(1)
        self.assertEqual(tst.loads[0].energy, 1)

        tst.add_load(2)
        self.assertEqual(tst.loads[0].energy, 2)
        self.assertEqual(tst.loads[1].energy, 1)

        tst.add_load(3)
        self.assertEqual(tst.loads[0].energy, 3)
        self.assertEqual(tst.loads[1].energy, 2)
        self.assertEqual(tst.loads[2].energy, 1)

        tst.add_load(4)
        self.assertEqual(tst.loads[0].energy, 4)
        self.assertEqual(tst.loads[1].energy, 3)
        self.assertEqual(tst.loads[2].energy, 3)

        tst.add_load(5)
        self.assertEqual(tst.loads[0].energy, 5)
        self.assertEqual(tst.loads[1].energy, 4)
        self.assertEqual(tst.loads[2].energy, 3)
        self.assertEqual(tst.loads[3].energy, 3)

        tst.add_load(6)
        self.assertEqual(tst.loads[0].energy, 6)
        self.assertEqual(tst.loads[1].energy, 5)
        self.assertEqual(tst.loads[2].energy, 7)
        self.assertEqual(tst.loads[3].energy, 3)

        tst.add_load(7)
        self.assertEqual(tst.loads[0].energy, 7)
        self.assertEqual(tst.loads[1].energy, 6)
        self.assertEqual(tst.loads[2].energy, 5)
        self.assertEqual(tst.loads[3].energy, 7)
        self.assertEqual(tst.loads[4].energy, 3)

        tst.add_load(8)
        self.assertEqual(tst.loads[0].energy, 8)
        self.assertEqual(tst.loads[1].energy, 7)
        self.assertEqual(tst.loads[2].energy, 11)
        self.assertEqual(tst.loads[3].energy, 7)
        self.assertEqual(tst.loads[4].energy, 3)

        tst.add_load(9)
        self.assertEqual(tst.loads[0].energy, 9)
        self.assertEqual(tst.loads[1].energy, 8)
        self.assertEqual(tst.loads[2].energy, 7)
        self.assertEqual(tst.loads[3].energy, 11)
        self.assertEqual(tst.loads[4].energy, 7)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.add_load(10)
        self.assertEqual(tst.loads[0].energy, 10)
        self.assertEqual(tst.loads[1].energy, 9)
        self.assertEqual(tst.loads[2].energy, 15)
        self.assertEqual(tst.loads[3].energy, 11)
        self.assertEqual(tst.loads[4].energy, 7)
        self.assertEqual(tst.loads[5].energy, 3)

        tst.add_load(11)
        self.assertEqual(tst.loads[0].energy, 11)
        self.assertEqual(tst.loads[1].energy, 10)
        self.assertEqual(tst.loads[2].energy, 9)
        self.assertEqual(tst.loads[3].energy, 15)
        self.assertEqual(tst.loads[4].energy, 11)
        self.assertEqual(tst.loads[5].energy, 10)

        tst.add_load(12)
        self.assertEqual(tst.loads[0].energy, 12)
        self.assertEqual(tst.loads[1].energy, 11)
        self.assertEqual(tst.loads[2].energy, 19)
        self.assertEqual(tst.loads[3].energy, 15)
        self.assertEqual(tst.loads[4].energy, 11)
        self.assertEqual(tst.loads[5].energy, 10)

        tst = StaticMethod()
        tst.add_load(1)
        self.assertEqual(tst.loads[0].energy, 1)
