import unittest

from glhe.profiles.profile_types import ProfileType


class TestProfileType(unittest.TestCase):

    def test_init(self):
        tst_external = ProfileType.EXTERNAL
        self.assertEqual(tst_external, ProfileType.EXTERNAL)

        tst_fixed = ProfileType.FIXED
        self.assertEqual(tst_fixed, ProfileType.FIXED)

        tst_single = ProfileType.IMPULSE
        self.assertEqual(tst_single, ProfileType.IMPULSE)

        tst_sinusoid = ProfileType.SINUSOID
        self.assertEqual(tst_sinusoid, ProfileType.SINUSOID)

        tst_synthetic = ProfileType.SYNTHETIC
        self.assertEqual(tst_synthetic, ProfileType.SYNTHETIC)
