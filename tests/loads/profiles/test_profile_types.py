import unittest

from loads.profiles.profile_types import ProfileType


class TestProfileType(unittest.TestCase):

    def test_init(self):
        tst_EXTERNAL = ProfileType.EXTERNAL
        self.assertEqual(tst_EXTERNAL, ProfileType.EXTERNAL)

        tst_FIXED = ProfileType.FIXED
        self.assertEqual(tst_FIXED, ProfileType.FIXED)

        tst_SINGLE = ProfileType.SINGLE_IMPULSE
        self.assertEqual(tst_SINGLE, ProfileType.SINGLE_IMPULSE)

        tst_SINUSOID = ProfileType.SINUSOID
        self.assertEqual(tst_SINUSOID, ProfileType.SINUSOID)

        tst_SYNTHETIC = ProfileType.SYNTHETIC
        self.assertEqual(tst_SYNTHETIC, ProfileType.SYNTHETIC)
