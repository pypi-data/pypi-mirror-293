import unittest
from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051',
    token='shs_qsdsq8d79qdsq65d4q6d84sqd68qsd64qsd48q68sf'
)

class TestProfiler(unittest.TestCase):
    @profiler.probe()
    def sample_function(self, start, end):
        return sum(range(start, end))

    def test_sample_function(self):
        result = self.sample_function(1, 1000)
        self.assertEqual(result, sum(range(1000)))

if __name__ == '__main__':
    unittest.main()