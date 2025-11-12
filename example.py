"""
Example usage of the Statistician package.

This script demonstrates various statistical functions available in the package.
"""

import numpy as np
import pandas as pd

from statistician import (
    confidence_interval,
    cut_outliers,
    homo_variance_test,
    mean,
    median,
    t_test,
)


def main():
    print("=" * 70)
    print("Statistician Package - Example Usage")
    print("=" * 70)

    # =================================================================
    # Example 1: Basic Descriptive Statistics
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 1: Basic Descriptive Statistics")
    print("=" * 70)

    data = [23, 25, 27, 24, 26, 28, 25, 24, 27, 26]
    print(f"\nData: {data}")
    print(f"Mean: {mean(data):.2f}")
    print(f"Median: {median(data):.2f}")

    # =================================================================
    # Example 2: Handling Messy Data
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 2: Handling Messy Data")
    print("=" * 70)

    messy_data = ["23", "25.5", None, "$27.00", " 29 ", "31.2", ""]
    print(f"\nMessy data: {messy_data}")
    print(f"Mean (auto-cleaned): {mean(messy_data):.2f}")
    print(f"Median (auto-cleaned): {median(messy_data):.2f}")

    # =================================================================
    # Example 3: Outlier Detection and Removal
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 3: Outlier Detection and Removal")
    print("=" * 70)

    df = pd.DataFrame({"scores": [85, 87, 88, 90, 92, 93, 150, 89, 91]})
    print(f"\nOriginal DataFrame:\n{df}")
    print(f"Mean with outlier: {mean(df['scores']):.2f}")

    # Remove outliers using IQR method
    df_clean = cut_outliers(df, "scores", method="q")
    print(f"\nCleaned DataFrame (IQR method):\n{df_clean}")
    print(f"Mean without outlier: {mean(df_clean['scores']):.2f}")

    # =================================================================
    # Example 4: Confidence Intervals
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 4: Confidence Intervals")
    print("=" * 70)

    # Small sample (uses t-distribution)
    small_sample = [12, 15, 14, 13, 16, 15, 14]
    ci_95 = confidence_interval(small_sample, confidence=0.95)
    ci_99 = confidence_interval(small_sample, confidence=0.99)

    print(f"\nSmall sample: {small_sample}")
    print(f"Sample mean: {mean(small_sample):.2f}")
    print(f"95% Confidence Interval: ({ci_95[0]:.2f}, {ci_95[1]:.2f})")
    print(f"99% Confidence Interval: ({ci_99[0]:.2f}, {ci_99[1]:.2f})")

    # =================================================================
    # Example 5: Two-Sample T-Test
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 5: Two-Sample T-Test")
    print("=" * 70)

    # Generate sample data
    np.random.seed(42)
    control = np.random.normal(loc=100, scale=15, size=30)
    treatment = np.random.normal(loc=110, scale=15, size=30)

    print(f"\nControl group mean: {mean(control):.2f}")
    print(f"Treatment group mean: {mean(treatment):.2f}")

    # Perform t-test
    results = t_test(control, treatment, alpha=0.05, equal_var=True)
    print(f"\nT-Test Results:")
    print(results)

    # =================================================================
    # Example 6: Variance Homogeneity Testing
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 6: Variance Homogeneity Testing")
    print("=" * 70)

    group1 = [12, 14, 15, 13, 16, 15, 14, 13, 15, 14]
    group2 = [22, 24, 23, 25, 26, 24, 23, 25, 24, 23]

    print(f"\nGroup 1: {group1}")
    print(f"Group 2: {group2}")

    variance_results = homo_variance_test(group1, group2, alpha=0.05)
    print(f"\nVariance Homogeneity Test Results:")
    print(variance_results)

    # =================================================================
    # Example 7: Complete Analysis Workflow
    # =================================================================
    print("\n" + "=" * 70)
    print("Example 7: Complete Analysis Workflow")
    print("=" * 70)

    # Simulate experiment data
    np.random.seed(123)
    df_experiment = pd.DataFrame(
        {
            "control": np.random.normal(loc=50, scale=10, size=25),
            "treatment": np.random.normal(loc=55, scale=10, size=25),
        }
    )

    # Add an outlier
    df_experiment.loc[0, "control"] = 150

    print("\n1. Original data (with outlier):")
    print(f"   Control mean: {mean(df_experiment['control']):.2f}")
    print(f"   Treatment mean: {mean(df_experiment['treatment']):.2f}")

    # Remove outliers
    df_experiment = cut_outliers(df_experiment, "control", method="z")

    print("\n2. After removing outliers:")
    print(f"   Control mean: {mean(df_experiment['control']):.2f}")
    print(f"   Treatment mean: {mean(df_experiment['treatment']):.2f}")

    # Check variance homogeneity
    print("\n3. Check variance homogeneity:")
    var_test = homo_variance_test(
        df_experiment["control"], df_experiment["treatment"]
    )
    print(var_test)

    # Perform appropriate t-test
    print("\n4. Perform t-test:")
    test_results = t_test(
        df_experiment["control"],
        df_experiment["treatment"],
        equal_var=True,  # Based on variance test
    )
    print(test_results)

    # Calculate confidence intervals
    print("\n5. Confidence intervals:")
    ci_control = confidence_interval(df_experiment["control"], confidence=0.95)
    ci_treatment = confidence_interval(df_experiment["treatment"], confidence=0.95)
    print(f"   Control 95% CI: ({ci_control[0]:.2f}, {ci_control[1]:.2f})")
    print(f"   Treatment 95% CI: ({ci_treatment[0]:.2f}, {ci_treatment[1]:.2f})")

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
