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

    def test_constant_single_and_empty(self):
        self.assertEqual(resample([0.25], 1, 3), [0.25] * 3)
        self.assertEqual(resample([], 2, 3), [])

    def test_invalid(self):
        for (samples, a, b) in [([float('nan')], 1, 2), ([2], 1, 2), ([0], 0, 2), ([0], True, 2), ([0], 1, 20000000)]:
            with self.assertRaises(ValueError):
                resample(samples, a, b)
if __name__ == '__main__':
    unittest.main()
