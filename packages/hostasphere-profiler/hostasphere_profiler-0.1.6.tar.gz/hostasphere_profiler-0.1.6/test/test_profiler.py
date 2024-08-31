import unittest
from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051',
    token='hsp_b3d7fe24e295269046b36cf504dfe60c1e7d4723d4821ddc3b30d1a5d057c28b'
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