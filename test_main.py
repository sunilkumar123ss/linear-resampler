import unittest
try:
    from .main import resample
except ImportError:
    from main import resample

class ResampleTests(unittest.TestCase):

    def test_identity(self):
        self.assertEqual(resample([0, 0.5, -0.5], 8000, 8000), [0, 0.5, -0.5])

    def test_linear_ramp(self):
        self.assertEqual(resample([0, 1], 2, 4), [0, 0.5, 1, 1])

    def test_downsample_and_length(self):
        self.assertEqual(resample([0, 0.25, 0.5, 0.75], 4, 2), [0, 0.5])
        self.assertEqual(len(resample([0] * 5, 3, 2)), 4)
