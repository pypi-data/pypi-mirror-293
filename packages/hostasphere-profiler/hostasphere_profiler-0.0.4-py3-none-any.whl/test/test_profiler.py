import unittest
from profiler.core import Profiler

profiler = Profiler(
    endpoint_url='http://localhost:5000',
    license_id='1234',
    license_secret='567'
)

class TestProfiler(unittest.TestCase):

    @profiler.probe()
    def sample_function(self):
        return sum(range(1000))

    def test_sample_function(self):
        result = self.sample_function()
        self.assertEqual(result, sum(range(1000)))

if __name__ == '__main__':
    unittest.main()