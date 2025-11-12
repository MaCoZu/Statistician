import unittest

import numpy as np

from statistician.inferential import confidence_interval, homo_variance_test, t_test


class TestInferential(unittest.TestCase):
    def test_confidence_interval(self):
        data = [1, 2, 3, 4, 5]
        ci = confidence_interval(data, confidence=0.95)
        self.assertEqual(len(ci), 2)
        self.assertIsInstance(ci, tuple)
        self.assertIsInstance(ci[0], float)
        self.assertIsInstance(ci[1], float)

    def test_t_test(self):
        data1 = [1, 2, 3, 4, 5]
        data2 = [2, 3, 4, 5, 6]
        result = t_test(data1, data2)
        self.assertIsNotNone(result)

    def test_homo_variance_test(self):
        group1 = [1, 2, 3, 4, 5]
        group2 = [2, 3, 4, 5, 6]
        result = homo_variance_test(group1, group2)
        self.assertEqual(len(result), 4)

if __name__ == '__main__':
    unittest.main()
