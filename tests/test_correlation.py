"""Tests for correlation analysis functions."""

import unittest

import numpy as np
import pandas as pd

from statistician.correlation import (
    correlation_matrix,
    pearson_correlation,
    spearman_correlation,
)


class TestPearsonCorrelation(unittest.TestCase):
    """Test cases for Pearson correlation."""

    def test_perfect_positive_correlation(self):
        """Test perfect positive linear correlation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        result = pearson_correlation(x, y)

        # Check result is DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Extract correlation coefficient
        r_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(r_value, 1.0, places=5)

    def test_perfect_negative_correlation(self):
        """Test perfect negative linear correlation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]

        result = pearson_correlation(x, y)

        r_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(r_value, -1.0, places=5)

    def test_no_correlation(self):
        """Test no correlation between variables."""
        x = [1, 2, 3, 4, 5]
        y = [3, 3, 3, 3, 3]  # Constant, no variation

        result = pearson_correlation(x, y)

        # Should have NaN or very small p-value
        self.assertIsInstance(result, pd.DataFrame)

    def test_moderate_correlation(self):
        """Test moderate correlation."""
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2.1, 4.2, 5.8, 8.1, 9.9, 12.2, 13.8, 16.1, 17.9, 20.2]

        result = pearson_correlation(x, y)

        r_value = float(result.loc[0, 'Value'])
        # Should be close to 1 but not perfect
        self.assertGreater(r_value, 0.9)
        self.assertLess(r_value, 1.0)

    def test_with_numpy_arrays(self):
        """Test Pearson correlation accepts numpy arrays."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])

        result = pearson_correlation(x, y)

        self.assertIsInstance(result, pd.DataFrame)
        r_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(r_value, 1.0, places=5)

    def test_with_pandas_series(self):
        """Test Pearson correlation accepts pandas Series."""
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([2, 4, 6, 8, 10])

        result = pearson_correlation(x, y)

        self.assertIsInstance(result, pd.DataFrame)

    def test_different_lengths_raises_error(self):
        """Test error raised when x and y have different lengths."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6]

        with self.assertRaises(ValueError) as context:
            pearson_correlation(x, y)

        self.assertIn("same length", str(context.exception))

    def test_empty_array_raises_error(self):
        """Test error raised with empty input."""
        x = []
        y = [1, 2, 3]

        with self.assertRaises(ValueError) as context:
            pearson_correlation(x, y)

        self.assertIn("empty", str(context.exception).lower())

    def test_single_value_raises_error(self):
        """Test error raised with insufficient data points."""
        x = [1]
        y = [2]

        with self.assertRaises(ValueError) as context:
            pearson_correlation(x, y)

        self.assertIn("At least 2", str(context.exception))

    def test_invalid_alpha_raises_error(self):
        """Test error raised with invalid alpha."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        with self.assertRaises(ValueError):
            pearson_correlation(x, y, alpha=1.5)

        with self.assertRaises(ValueError):
            pearson_correlation(x, y, alpha=-0.5)

    def test_significance_detection(self):
        """Test that significance is correctly detected."""
        # Strong correlation should be significant
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

        result = pearson_correlation(x, y, alpha=0.05)

        # Check significance field
        sig_value = result.loc[2, 'Value']
        self.assertEqual(sig_value, 'True')

    def test_result_structure(self):
        """Test that result has expected structure."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        result = pearson_correlation(x, y)

        # Check columns exist
        self.assertIn('Statistic', result.columns)
        self.assertIn('Value', result.columns)

        # Check expected statistics are present
        stats = result['Statistic'].tolist()
        self.assertIn('Correlation Coefficient (r)', stats)
        self.assertIn('P-value', stats)
        self.assertIn('Sample Size', stats)

    def test_with_messy_data(self):
        """Test correlation handles messy data through clean_to_numeric_array."""
        x = ['1', '2', '3', '4', '5']
        y = ['2', '4', '6', '8', '10']

        result = pearson_correlation(x, y)

        r_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(r_value, 1.0, places=5)


class TestSpearmanCorrelation(unittest.TestCase):
    """Test cases for Spearman correlation."""

    def test_perfect_monotonic_correlation(self):
        """Test perfect monotonic relationship."""
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]  # Non-linear but monotonic

        result = spearman_correlation(x, y)

        # Check result is DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Spearman should detect perfect monotonic relationship
        rho_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(rho_value, 1.0, places=5)

    def test_negative_monotonic_correlation(self):
        """Test negative monotonic relationship."""
        x = [1, 2, 3, 4, 5]
        y = [25, 16, 9, 4, 1]

        result = spearman_correlation(x, y)

        rho_value = float(result.loc[0, 'Value'])
        self.assertAlmostEqual(rho_value, -1.0, places=5)

    def test_with_tied_ranks(self):
        """Test Spearman with tied ranks."""
        x = [1, 2, 2, 3, 4]
        y = [2, 3, 3, 4, 5]

        result = spearman_correlation(x, y)

        # Should handle ties correctly
        self.assertIsInstance(result, pd.DataFrame)
        rho_value = float(result.loc[0, 'Value'])
        self.assertGreater(rho_value, 0)

    def test_different_lengths_raises_error(self):
        """Test error raised when x and y have different lengths."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6]

        with self.assertRaises(ValueError) as context:
            spearman_correlation(x, y)

        self.assertIn("same length", str(context.exception))

    def test_empty_array_raises_error(self):
        """Test error raised with empty input."""
        x = []
        y = [1, 2, 3]

        with self.assertRaises(ValueError):
            spearman_correlation(x, y)

    def test_single_value_raises_error(self):
        """Test error raised with insufficient data points."""
        x = [1]
        y = [2]

        with self.assertRaises(ValueError):
            spearman_correlation(x, y)

    def test_invalid_alpha_raises_error(self):
        """Test error raised with invalid alpha."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        with self.assertRaises(ValueError):
            spearman_correlation(x, y, alpha=1.5)

    def test_result_structure(self):
        """Test that result has expected structure."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        result = spearman_correlation(x, y)

        # Check columns exist
        self.assertIn('Statistic', result.columns)
        self.assertIn('Value', result.columns)

        # Check expected statistics are present
        stats = result['Statistic'].tolist()
        self.assertIn('Correlation Coefficient (ρ)', stats)
        self.assertIn('P-value', stats)
        self.assertIn('Sample Size', stats)

    def test_spearman_vs_pearson_with_outliers(self):
        """Test that Spearman is more robust to outliers than Pearson."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 1000]  # Last value is outlier

        spearman_result = spearman_correlation(x, y)
        pearson_result = pearson_correlation(x, y)

        spearman_rho = float(spearman_result.loc[0, 'Value'])
        pearson_r = float(pearson_result.loc[0, 'Value'])

        # Spearman should be less affected (closer to 1)
        # This tests robustness to outliers
        self.assertGreater(abs(spearman_rho), abs(pearson_r))


class TestCorrelationMatrix(unittest.TestCase):
    """Test cases for correlation matrix."""

    def test_basic_correlation_matrix(self):
        """Test basic correlation matrix calculation."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10],
            'c': [5, 4, 3, 2, 1]
        })

        corr_matrix, p_matrix = correlation_matrix(df, method='pearson')

        # Check types
        self.assertIsInstance(corr_matrix, pd.DataFrame)
        self.assertIsInstance(p_matrix, pd.DataFrame)

        # Check shape
        self.assertEqual(corr_matrix.shape, (3, 3))
        self.assertEqual(p_matrix.shape, (3, 3))

        # Check diagonal is 1 (correlation with self)
        self.assertEqual(corr_matrix.loc['a', 'a'], 1.0)
        self.assertEqual(corr_matrix.loc['b', 'b'], 1.0)
        self.assertEqual(corr_matrix.loc['c', 'c'], 1.0)

        # Check symmetry
        self.assertAlmostEqual(
            corr_matrix.loc['a', 'b'],
            corr_matrix.loc['b', 'a'],
            places=10
        )

    def test_correlation_matrix_with_perfect_correlation(self):
        """Test correlation matrix identifies perfect correlations."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 6, 8, 10],  # Perfect positive with x
            'z': [5, 4, 3, 2, 1]    # Perfect negative with x
        })

        corr_matrix, p_matrix = correlation_matrix(df)

        # x and y should have correlation close to 1
        self.assertAlmostEqual(corr_matrix.loc['x', 'y'], 1.0, places=5)

        # x and z should have correlation close to -1
        self.assertAlmostEqual(corr_matrix.loc['x', 'z'], -1.0, places=5)

    def test_spearman_method(self):
        """Test correlation matrix with Spearman method."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [1, 4, 9, 16, 25],
            'c': [2, 3, 4, 5, 6]
        })

        corr_matrix, p_matrix = correlation_matrix(df, method='spearman')

        self.assertIsInstance(corr_matrix, pd.DataFrame)
        self.assertEqual(corr_matrix.shape, (3, 3))

    def test_invalid_method_raises_error(self):
        """Test error raised with invalid correlation method."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10]
        })

        with self.assertRaises(ValueError) as context:
            correlation_matrix(df, method='invalid')

        self.assertIn("pearson", str(context.exception).lower())

    def test_non_dataframe_raises_error(self):
        """Test error raised when input is not a DataFrame."""
        data = [[1, 2, 3], [4, 5, 6]]

        with self.assertRaises(ValueError) as context:
            correlation_matrix(data)

        self.assertIn("DataFrame", str(context.exception))

    def test_single_column_raises_error(self):
        """Test error raised with insufficient columns."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5]
        })

        with self.assertRaises(ValueError) as context:
            correlation_matrix(df)

        self.assertIn("at least 2", str(context.exception))

    def test_non_numeric_columns_ignored(self):
        """Test that non-numeric columns are properly handled."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10],
            'c': ['x', 'y', 'z', 'w', 'v']  # Non-numeric
        })

        corr_matrix, p_matrix = correlation_matrix(df)

        # Should only include numeric columns
        self.assertEqual(corr_matrix.shape, (2, 2))
        self.assertIn('a', corr_matrix.columns)
        self.assertIn('b', corr_matrix.columns)
        self.assertNotIn('c', corr_matrix.columns)

    def test_with_missing_values(self):
        """Test correlation matrix handles missing values."""
        df = pd.DataFrame({
            'a': [1, 2, np.nan, 4, 5],
            'b': [2, 4, 6, np.nan, 10],
            'c': [5, 4, 3, 2, 1]
        })

        corr_matrix, p_matrix = correlation_matrix(df)

        # Should calculate pairwise complete correlations
        self.assertIsInstance(corr_matrix, pd.DataFrame)
        self.assertEqual(corr_matrix.shape, (3, 3))

    def test_p_values_on_diagonal_are_zero(self):
        """Test that p-values on diagonal are 0."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10],
            'c': [5, 4, 3, 2, 1]
        })

        corr_matrix, p_matrix = correlation_matrix(df)

        # P-values for self-correlation should be 0
        self.assertEqual(p_matrix.loc['a', 'a'], 0.0)
        self.assertEqual(p_matrix.loc['b', 'b'], 0.0)
        self.assertEqual(p_matrix.loc['c', 'c'], 0.0)

    def test_invalid_alpha_raises_error(self):
        """Test error raised with invalid alpha."""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10]
        })

        with self.assertRaises(ValueError):
            correlation_matrix(df, alpha=1.5)


if __name__ == '__main__':
    unittest.main()
