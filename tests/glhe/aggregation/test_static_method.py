import unittest

from glhe.aggregation.static_method import StaticMethod


class TestStatic(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {'minimum-num-bins-for-each-level': [2, 2, 2],
             'bin-durations-in-hours': [1, 2, 4]}

        return StaticMethod(d)

    def test_aggregate(self):
        tst = self.add_instance()

        t = 0
        dt = 3600

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)

        t += dt
        tst.aggregate(t, 4)
