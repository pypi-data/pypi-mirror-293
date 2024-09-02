import unittest
from my_sample_package.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3, 4, 5]
        self.processor = DataProcessor(self.data)

    def test_sum(self):
        self.assertEqual(self.processor.sum(), 15)

    def test_average(self):
        self.assertEqual(self.processor.average(), 3)

if __name__ == '__main__':
    unittest.main()
