import unittest

from glhe.ground_temps.two_harmonic import TwoHarmonic


class TestTwoHarmonic(unittest.TestCase):

    def test_two_harmonic_ground_temp(self):
        tol = 1e-4

        inputs = {'soil-diffusivity': 1e-6,
                  'average-temperature': 15,
                  'amplitude-1': 0,
                  'amplitude-2': 0,
                  'phase-shift-1': 0,
                  'phase-shift-2': 0}

        tst = TwoHarmonic(inputs)
        self.assertAlmostEqual(tst.get_temp(0, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(15768000, 0), 15, delta=tol)
        self.assertAlmostEqual(tst.get_temp(15768000, 100), 15, delta=tol)

        inputs['amplitude-1'] = 5

        tst = TwoHarmonic(inputs)
        self.assertAlmostEqual(tst.get_temp(0, 0), 10, delta=tol)
        self.assertAlmostEqual(tst.get_temp(0, 100), 15, delta=tol)

        self.assertAlmostEqual(tst.get_temp(15768000, 0), 20, delta=tol)
        self.assertAlmostEqual(tst.get_temp(15768000, 100), 15, delta=tol)
