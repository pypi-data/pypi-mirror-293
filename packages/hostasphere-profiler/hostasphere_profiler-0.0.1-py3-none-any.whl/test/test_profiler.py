import unittest
from profiler import probe

class TestProfiler(unittest.TestCase):

    @probe()
    def sample_function(self):
        return sum(range(1000))

    def test_sample_function(self):
        result = self.sample_function()
        self.assertEqual(result, sum(range(1000)))

if __name__ == '__main__':
    unittest.main()