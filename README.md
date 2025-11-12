# Statistician

[![PyPI version](https://badge.fury.io/py/statistician.svg)](https://badge.fury.io/py/statistician)
[![Python Versions](https://img.shields.io/pypi/pyversions/statistician.svg)](https://pypi.org/project/statistician/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/MaCoZu/statistician/workflows/Tests/badge.svg)](https://github.com/MaCoZu/statistician/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Statistician** is a Python package that provides a comprehensive collection of statistical functions for data analysis and hypothesis testing. It simplifies complex statistical operations with an intuitive API and robust data handling.

## ✨ Features

- **Descriptive Statistics**: Calculate mean, median, and handle outliers
- **Confidence Intervals**: Automatic distribution selection (t vs normal)
- **Hypothesis Testing**: Two-sample t-tests with pooled and Welch's variants
- **Variance Testing**: Multiple methods (F-test, Levene's, Bartlett's)
- **Robust Data Cleaning**: Automatically handles dirty data, missing values, and type conversions
- **Flexible Input**: Supports lists, NumPy arrays, Pandas Series, and more
- **Type Hints**: Full type annotation support for better IDE integration

## 📦 Installation

Install Statistician using pip:

```bash
pip install statistician
```

For development with additional tools:

```bash
pip install statistician[dev]
```

## 🚀 Quick Start

```python
from statistician import mean, median, confidence_interval, t_test

# Basic statistics
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Mean: {mean(data)}")          # Mean: 5.5
print(f"Median: {median(data)}")      # Median: 5.5

# Confidence interval
ci = confidence_interval(data, confidence=0.95)
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")

# Two-sample t-test
group1 = [23, 25, 27, 29, 31]
group2 = [33, 35, 37, 39, 41]
results = t_test(group1, group2)
print(results)
```

## 📚 Documentation

### Descriptive Statistics

#### `mean(data)`

Calculate the arithmetic mean of the data.

```python
from statistician import mean

data = [1, 2, 3, 4, 5]
result = mean(data)  # 3.0

# Handles dirty data automatically
messy_data = ['1', '2.5', None, '3', ' 4.5 ', '$5.00']
result = mean(messy_data)  # 3.2
```

**Parameters:**
- `data` (array-like): Input data

**Returns:**
- `float`: The arithmetic mean

---

#### `median(data)`

Calculate the median of the data.

```python
from statistician import median

data = [1, 2, 3, 4, 5]
result = median(data)  # 3.0

# Works with any array-like structure
import pandas as pd
df = pd.DataFrame({'values': [10, 20, 30, 40, 50]})
result = median(df['values'])  # 30.0
```

**Parameters:**
- `data` (array-like): Input data

**Returns:**
- `float`: The median value

---

#### `cut_outliers(df, col, method='q')`

Remove outliers from a DataFrame based on specified column.

```python
from statistician import cut_outliers
import pandas as pd

df = pd.DataFrame({'scores': [85, 87, 88, 90, 92, 93, 150]})

# Using IQR method (default)
df_clean = cut_outliers(df, 'scores', method='q')

# Using z-score method
df_clean = cut_outliers(df, 'scores', method='z')
```

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `col` (str): Column name to check for outliers
- `method` (str): Method to use - 'q' for IQR (default) or 'z' for z-score

**Returns:**
- `pd.DataFrame`: DataFrame with outliers removed

**Methods:**
- `'q'`: IQR method (removes values < Q1-1.5×IQR or > Q3+1.5×IQR)
- `'z'`: Z-score method (removes values with |z| > 3)

---

### Inferential Statistics

#### `confidence_interval(data, confidence=0.95, pop_std=None)`

Calculate the confidence interval for the population mean.

```python
from statistician import confidence_interval

# Small sample (uses t-distribution)
sample = [12, 15, 14, 13, 16, 15, 14]
ci = confidence_interval(sample, confidence=0.95)
print(f"95% CI: {ci}")  # (13.15, 15.42)

# Large sample (uses normal distribution)
large_sample = list(range(1, 101))
ci = confidence_interval(large_sample, confidence=0.99)

# With known population standard deviation
ci = confidence_interval(sample, confidence=0.95, pop_std=2.5)
```

**Parameters:**
- `data` (array-like): Sample data
- `confidence` (float): Confidence level (default: 0.95)
- `pop_std` (float, optional): Population standard deviation if known

**Returns:**
- `tuple`: (lower_bound, upper_bound)

**Behavior:**
- Uses t-distribution for n ≤ 30 (small samples)
- Uses normal distribution for n > 30 (large samples)
- Uses normal distribution if population std is provided

---

#### `t_test(data_1, data_2, alpha=0.05, expected_diff=0, equal_var=True)`

Perform a two-sample independent t-test.

```python
from statistician import t_test

# Compare two groups
control = [23, 25, 27, 24, 26]
treatment = [30, 32, 31, 33, 29]

# Standard pooled t-test (assumes equal variances)
results = t_test(control, treatment)
print(results)

# Welch's t-test (doesn't assume equal variances)
results = t_test(control, treatment, equal_var=False)

# One-tailed test with alpha = 0.01
results = t_test(control, treatment, alpha=0.01)

# Test for specific difference
results = t_test(control, treatment, expected_diff=5)
```

**Parameters:**
- `data_1` (array-like): First sample data
- `data_2` (array-like): Second sample data
- `alpha` (float): Significance level (default: 0.05)
- `expected_diff` (float): Hypothesized difference μ₁-μ₂ (default: 0)
- `equal_var` (bool): Assume equal variances (default: True)

**Returns:**
- `pd.DataFrame`: Comprehensive test results including:
  - Means and variances
  - t-statistic
  - p-values (one-tail and two-tail)
  - Critical values
  - Degrees of freedom

---

#### `homo_variance_test(group1, group2, alpha=0.05)`

Test homogeneity of variance between two groups using multiple methods.

```python
from statistician import homo_variance_test

group1 = [12, 14, 15, 13, 16, 15]
group2 = [22, 24, 23, 25, 26, 24]

results = homo_variance_test(group1, group2)
print(results)
```

**Parameters:**
- `group1` (array-like): First group data
- `group2` (array-like): Second group data
- `alpha` (float): Significance level (default: 0.05)

**Returns:**
- `pd.DataFrame`: Results from four tests:
  - **Rule of thumb**: Variance ratio ≤ 4
  - **F-test**: Parametric test (assumes normality)
  - **Levene's test**: Robust to non-normality
  - **Bartlett's test**: Most powerful if data is normal

**Output includes:**
- Test name
- Result (equal/not equal variances)
- Reasoning (test statistic or p-value)

---

## 🧪 Examples

### Complete Analysis Workflow

```python
import pandas as pd
from statistician import (
    mean, median, cut_outliers,
    confidence_interval, t_test, homo_variance_test
)

# Load data
df = pd.DataFrame({
    'control': [23, 25, 27, 24, 26, 28, 100],  # Note the outlier
    'treatment': [30, 32, 31, 33, 29, 34, 30]
})

# 1. Remove outliers
df = cut_outliers(df, 'control', method='q')

# 2. Descriptive statistics
print(f"Control mean: {mean(df['control']):.2f}")
print(f"Treatment mean: {mean(df['treatment']):.2f}")

# 3. Check variance homogeneity
variance_test = homo_variance_test(df['control'], df['treatment'])
print("\nVariance Tests:")
print(variance_test)

# 4. Perform appropriate t-test
results = t_test(df['control'], df['treatment'], equal_var=True)
print("\nT-Test Results:")
print(results)

# 5. Calculate confidence intervals
ci_control = confidence_interval(df['control'])
ci_treatment = confidence_interval(df['treatment'])
print(f"\nControl 95% CI: ({ci_control[0]:.2f}, {ci_control[1]:.2f})")
print(f"Treatment 95% CI: ({ci_treatment[0]:.2f}, {ci_treatment[1]:.2f})")
```

### Handling Real-World Messy Data

```python
from statistician import mean, median

# Data with various issues
messy_data = [
    '23', '25.5', None, '$27.00', ' 29 ', 
    '31.2', 'N/A', '33,456.78', ''
]

# Automatically cleaned and converted
print(f"Mean: {mean(messy_data)}")
print(f"Median: {median(messy_data)}")
```

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/MaCoZu/statistician.git
cd statistician

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black statistician/ tests/
isort statistician/ tests/
```

## 📋 Requirements

- Python ≥ 3.8
- NumPy ≥ 1.20.0
- Pandas ≥ 1.2.0
- SciPy ≥ 1.6.0

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Project Status

**Status**: Alpha

Statistician is under active development. The API is stable for the current features, but new functions and improvements are being added regularly.

## 🗺️ Roadmap

- [ ] ANOVA (one-way and two-way)
- [ ] Chi-square tests
- [ ] Correlation analysis (Pearson, Spearman)
- [ ] Non-parametric tests (Mann-Whitney, Wilcoxon)
- [ ] Power analysis
- [ ] Effect size calculations
- [ ] Data visualization utilities
- [ ] Comprehensive documentation site

## 📧 Contact

**Marco Zausch** - marcoz@posteo.de

Project Link: [https://github.com/MaCoZu/statistician](https://github.com/MaCoZu/statistician)

## 🙏 Acknowledgments

- Built with [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/), and [SciPy](https://scipy.org/)
- Inspired by the need for simpler statistical testing in Python
- Thanks to all contributors who help improve this package

---

**Made with ❤️ for the data science community**