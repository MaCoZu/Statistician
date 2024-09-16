import unittest
import numpy as np
import pandas as pd
from statistician.descriptive import mean, median, cut_outliers

class TestDescriptive(unittest.TestCase):
    def test_mean(self):
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(mean(data), 3.0)

    def test_median(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(median(data), 3.0)

    def test_cut_outliers(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 100]})
        df_cleaned = cut_outliers(df, 'A', method='z')
        self.assertEqual(len(df_cleaned), 4)

if __name__ == '__main__':
    unittest.main()