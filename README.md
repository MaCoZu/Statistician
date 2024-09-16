# Statistician

Statistician is a Python package that provides a collection of statistical functions for data analysis and inference.

## Features

- Descriptive statistics (mean, median)
- Outlier detection and removal
- Confidence interval calculation
- T-test for comparing two samples
- Homogeneity of variance test

## Installation

You can install Statistician using pip:

```
pip install statistician
```

## Usage

Here's a quick example of how to use Statistician:

```python
from statistician import mean, median, confidence_interval, t_test

# Calculate basic statistics
data = [1, 2, 3, 4, 5]
print(f"Mean: {mean(data)}")
print(f"Median: {median(data)}")

# Calculate confidence interval
ci = confidence_interval(data, confidence=0.95)
print(f"95% Confidence Interval: {ci}")

# Perform t-test
data1 = [1, 2, 3, 4, 5]
data2 = [2, 3, 4, 5, 6]
t_test_result = t_test(data1, data2)
print("T-test results:")
print(t_test_result)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.