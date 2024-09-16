from statistician import mean, median, confidence_interval, t_test, homo_variance_test
import numpy as np

# Generate some sample data
np.random.seed(42)
data1 = np.random.normal(loc=5, scale=2, size=100)
data2 = np.random.normal(loc=6, scale=2, size=100)

# Calculate basic statistics
print(f"Data 1 - Mean: {mean(data1):.2f}, Median: {median(data1):.2f}")
print(f"Data 2 - Mean: {mean(data2):.2f}, Median: {median(data2):.2f}")

# Calculate confidence interval
ci = confidence_interval(data1, confidence=0.95)
print(f"\n95% Confidence Interval for Data 1: {ci[1]}")

# Perform t-test
t_test_result = t_test(data1, data2)
print("\nT-test results:")
print(t_test_result)

# Perform homogeneity of variance test
homo_var_result = homo_variance_test(data1, data2)
print("\nHomogeneity of Variance Test results:")
print(homo_var_result)