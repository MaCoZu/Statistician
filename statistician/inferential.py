import math

import numpy as np
import pandas as pd
import scipy.stats as st

from .descriptive import clean_to_numeric_array

# Constants
SMALL_SAMPLE_THRESHOLD = 30
VARIANCE_RATIO_THRESHOLD = 4


def confidence_interval(data, confidence=0.95, pop_std=None):
    """
    Calculates the confidence interval (CI) for the population mean.

    A CI for the population mean provides a range within which the true population mean
    is likely to lie, based on a sample.

    You provide a confidence level that you want to have in saying the true mean lies
    within that interval. The CI represents the range of values that contain the true
    mean with that confidence. The more confident you want to be, the wider the CI
    becomes to ensure the true mean lies within it.

    - Uses t-distribution for n <= 30 (small samples)
    - Uses Normal distribution for n > 30 (large samples)
    - If population standard deviation is provided, the standard error of the mean (SEM)
      is calculated with it and normal distribution is used.

    Args:
        data (array-like): Data sample.
        confidence (float): Level of confidence (e.g., 0.95 for 95% confidence).
            Must be between 0 and 1.
        pop_std (float, optional): Population standard deviation. Defaults to None.

    Returns:
        tuple: (lower_bound, upper_bound) of the confidence interval.

    Raises:
        ValueError: If confidence is not between 0 and 1, or if data is empty.
    """
    if not 0 < confidence < 1:
        raise ValueError("Confidence level must be between 0 and 1")

    data = clean_to_numeric_array(data)

    if len(data) == 0:
        raise ValueError("Data cannot be empty")

    n = len(data)
    mean = np.mean(data)

    # If population standard deviation is provided, use normal distribution
    if pop_std is not None:
        if pop_std <= 0:
            raise ValueError("Population standard deviation must be positive")
        sem = pop_std / np.sqrt(n)
        conf_interval = st.norm.interval(confidence, loc=mean, scale=sem)
    # Use t-distribution for small samples (n <= 30)
    elif n <= SMALL_SAMPLE_THRESHOLD:
        conf_interval = st.t.interval(confidence, df=n - 1, loc=mean, scale=st.sem(data))
    # Use normal distribution for large samples (n > 30)
    else:
        conf_interval = st.norm.interval(confidence, loc=mean, scale=st.sem(data))

    # Convert np.float64 to plain Python float for better compatibility
    return (float(conf_interval[0]), float(conf_interval[1]))


def t_test(data_1, data_2, alpha=0.05, expected_diff=0, equal_var=True):
    """
    Perform a two-sample independent t-test.

    Tests whether the means of two independent samples are significantly different.

    Args:
        data_1 (array-like): First sample data.
        data_2 (array-like): Second sample data.
        alpha (float, optional): Significance level. Defaults to 0.05.
        expected_diff (float, optional): Hypothesized difference in means (mu1 - mu2).
            Defaults to 0.
        equal_var (bool, optional): Whether to assume equal variances (pooled t-test).
            If False, performs Welch's t-test. Defaults to True.

    Returns:
        pandas.DataFrame: DataFrame containing t-test statistics including means,
            variances, t-statistic, p-values, and critical values.

    Raises:
        ValueError: If data is invalid or alpha is not between 0 and 1.
    """
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")

    data_1 = clean_to_numeric_array(data_1)
    data_2 = clean_to_numeric_array(data_2)

    if len(data_1) < 2 or len(data_2) < 2:
        raise ValueError("Each sample must have at least 2 observations")

    confidence = 1 - alpha
    x1_bar = np.mean(data_1)
    x2_bar = np.mean(data_2)
    n_1 = len(data_1)
    n_2 = len(data_2)
    s1_squared = np.var(data_1, ddof=1)
    s2_squared = np.var(data_2, ddof=1)

    if equal_var:
        # Pooled t-test (assumes equal variances)
        pooled_df = n_1 + n_2 - 2
        pooled_variance = ((n_1 - 1) * s1_squared + (n_2 - 1) * s2_squared) / pooled_df
        se = math.sqrt(pooled_variance * (1 / n_1 + 1 / n_2))
        t_statistic = (x1_bar - x2_bar - expected_diff) / se
    else:
        # Welch's t-test (does not assume equal variances)
        se = math.sqrt(s1_squared / n_1 + s2_squared / n_2)
        t_statistic = (x1_bar - x2_bar - expected_diff) / se

        # Welch-Satterthwaite degrees of freedom
        numerator = (s1_squared / n_1 + s2_squared / n_2) ** 2
        denominator = (s1_squared / n_1) ** 2 / (n_1 - 1) + (s2_squared / n_2) ** 2 / (n_2 - 1)
        pooled_df = numerator / denominator
        pooled_variance = s1_squared / n_1 + s2_squared / n_2

    # One-tailed test
    p_one_tail = 1 - st.t.cdf(abs(t_statistic), pooled_df)
    t_critical_one_tail = st.t.ppf(confidence, df=pooled_df)

    # Two-tailed test
    p_two_tail = 2 * (1 - st.t.cdf(abs(t_statistic), pooled_df))
    t_critical_two_tail = st.t.ppf((1 + confidence) / 2, df=pooled_df)

    # Create results DataFrame
    df = pd.DataFrame({
        "t-test statistics": [
            "Mean",
            "Variance",
            "Observations",
            "Pooled Variance",
            "Hypothesized Mean Difference",
            "df",
            "t-statistic",
            "P(T<=t) one-tail",
            "t critical one-tail",
            "P(T<=t) two-tail",
            "t critical two-tail",
        ],
        "data_1": [
            x1_bar,
            s1_squared,
            n_1,
            pooled_variance,
            expected_diff,
            pooled_df,
            t_statistic,
            p_one_tail,
            t_critical_one_tail,
            p_two_tail,
            t_critical_two_tail,
        ],
        "data_2": [
            x2_bar,
            s2_squared,
            n_2,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ],
    }).set_index("t-test statistics")

    return df


def homo_variance_test(group1, group2, alpha=0.05):
    """
    Perform various tests to check the homogeneity of variance between two groups.

    This function conducts a series of tests to evaluate whether two groups have
    equal variances:

    1. Rule of thumb: Compares the ratio of the larger variance to the smaller variance.
       If ratio <= 4, variances are considered approximately equal.
    2. F-test: A parametric test that compares the variances of two groups.
       Assumes data is normally distributed.
    3. Levene's test: A robust non-parametric test that checks the equality of variances.
       Less sensitive to departures from normality.
    4. Bartlett's test: A parametric test for homogeneity of variances.
       More powerful but sensitive to normality assumptions.

    Args:
        group1 (array-like): The first group of data.
        group2 (array-like): The second group of data.
        alpha (float, optional): Significance level for the tests. Defaults to 0.05.

    Returns:
        pandas.DataFrame: A DataFrame containing the test names, results, and reasoning.

    Raises:
        ValueError: If data is invalid or alpha is not between 0 and 1.
    """
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")

    group1 = clean_to_numeric_array(group1)
    group2 = clean_to_numeric_array(group2)

    if len(group1) < 2 or len(group2) < 2:
        raise ValueError("Each group must have at least 2 observations")

    # Calculate variances
    s_1 = np.var(group1, ddof=1)
    s_2 = np.var(group2, ddof=1)

    if s_1 <= 0 or s_2 <= 0:
        raise ValueError("Variance cannot be zero or negative")

    # Rule of thumb test
    s_max = max(s_1, s_2)
    s_min = min(s_1, s_2)
    f_ratio = s_max / s_min
    rot_result = f_ratio <= VARIANCE_RATIO_THRESHOLD

    # F-test for equality of variances
    n1 = len(group1)
    n2 = len(group2)
    df1 = n1 - 1
    df2 = n2 - 1

    # Calculate F-statistic (ratio of variances)
    f_statistic = s_1 / s_2 if s_1 >= s_2 else s_2 / s_1

    # Two-tailed p-value for F-test
    if s_1 >= s_2:
        f_p_value = 2 * min(st.f.cdf(f_statistic, df1, df2),
                            1 - st.f.cdf(f_statistic, df1, df2))
    else:
        f_p_value = 2 * min(st.f.cdf(f_statistic, df2, df1),
                            1 - st.f.cdf(f_statistic, df2, df1))

    # Levene's test
    l_statistic, l_p_value = st.levene(group1, group2)

    # Bartlett's test
    b_statistic, b_p_value = st.bartlett(group1, group2)

    # Create results DataFrame
    results = {
        "Test": [
            "Rule of thumb",
            "F-test",
            "Levene's test",
            "Bartlett's test"
        ],
        "Result": [
            "Variances are equal" if rot_result else "Variances are not equal",
            "Variances are equal" if f_p_value > alpha else "Variances are not equal",
            "Variances are equal" if l_p_value > alpha else "Variances are not equal",
            "Variances are equal" if b_p_value > alpha else "Variances are not equal",
        ],
        "Reasoning": [
            f"{s_max:.4f} / {s_min:.4f} = {f_ratio:.4f} (threshold: {VARIANCE_RATIO_THRESHOLD})",
            f"p-value = {f_p_value:.6f} (alpha = {alpha})",
            f"p-value = {l_p_value:.6f} (alpha = {alpha})",
            f"p-value = {b_p_value:.6f} (alpha = {alpha})",
        ]
    }

    df_result = pd.DataFrame(results)
    return df_result
