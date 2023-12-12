import unittest
try:
    from .main import resample
except ImportError:
    from main import resample

class ResampleTests(unittest.TestCase):

    def test_identity(self):
        self.assertEqual(resample([0, 0.5, -0.5], 8000, 8000), [0, 0.5, -0.5])
