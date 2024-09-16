import math
import numpy as np
import pandas as pd
import scipy.stats as st

from .descriptive import clean_to_numeric_array

def confidence_interval(data, confidence=0.95, pop_std=None):
    """
    Calculates the confidence interval (CI) for the population mean.
    
    A CI for the population mean provides a range within which the true population mean 
    is likely to lie, based on a sample. 
    
    You provide a confidence, that you want to have in saying the true mean lies within that interval. 
    And the CI represets the range of values that contain the true mean with that confidence.
    The more confident you want to be the wider becomes the CI to make sure the true mean lies within it.
    
    - Uses t-distribution for n<=30
    - Uses Normal distribution for n>30
    - If populations standard deviation is provided the 
      standard error of the mean (sem) is calculated with it.

    Args:
        data (array-like): Data sample.
        confidence (float): Level of confidence (e.g., 0.95 for 95% confidence).
        pop_std (float, optional): Population standard deviation. Defaults to None.

    Returns:
        tuple: Lower and upper bounds of the confidence interval.
    """
    data = clean_to_numeric_array(data)
    n = len(data)
    mean = np.mean(data)

    # uses t-distribution for less than 30 observations
    if not pop_std and n <= 30:
        conf_interval = st.t.interval(confidence, df=n - 1, loc=mean, scale=st.sem(data))
        
    # normal-dist for n>30
    elif not pop_std and n > 30:
        conf_interval = st.norm.interval(confidence, loc=mean, scale=st.sem(data))
        
    # if population standard deviation is provided 
    # normal-dist is used & standard error of the mean is calculated with pop_std.
    else:
        sem = pop_std / np.sqrt(n)
        conf_interval = st.norm.interval(confidence, loc=mean, scale=sem)
        
    # Convert np.float64 to plain Python float
    return f"{confidence*100}% CI interval for population mean:", (float(conf_interval[0]), float(conf_interval[1]))

def t_test(data_1, data_2, alpha=0.05, expected_diff=0, equal_var=True):
    """
    Perform a two-sample t-test.

    Args:
        data_1 (array-like): First sample data.
        data_2 (array-like): Second sample data.
        alpha (float, optional): Significance level. Defaults to 0.05.
        expected_diff (int, optional): Expected difference in means. Defaults to 0.
        equal_var (bool, optional): Whether to assume equal variances. Defaults to True.

    Returns:
        pandas.DataFrame: DataFrame containing t-test statistics.
    """
    confidence = 1 - alpha
    x1_bar = np.mean(data_1)
    x2_bar = np.mean(data_2)
    n_1 = int(len(data_1))
    n_2 = int(len(data_2))
    pooled_df = n_1 + n_2 - 2
    s1_squared = np.var(data_1, ddof=1)
    s2_squared = np.var(data_2, ddof=1)

    if equal_var:
        # t-statistic for equal variance
        numerator = x1_bar - x2_bar - expected_diff
        pooled_variance = ((n_1 - 1) * s1_squared + (n_2 - 1) * s2_squared) / (pooled_df)
        denominator = math.sqrt(pooled_variance * ((1 / n_1) + (1 / n_2)))
        t_statistic = numerator / denominator
    else:
        numerator = x1_bar - x2_bar - expected_diff
        pooled_variance = (s1_squared / n_1) + (s2_squared / n_2)
        denominator = math.sqrt(pooled_variance)
        t_statistic = numerator / denominator

    # p and critical value for one-tailed test
    p_one_tail = 1 - st.t.cdf(abs(t_statistic), pooled_df)
    t_critical_one_tail = st.t.ppf(confidence, df=pooled_df)

    # p and critical value for two-tailed test
    p_two_tail = 2 * (1 - st.t.cdf(abs(t_statistic), pooled_df))
    t_critical_two_tail = st.t.ppf((1 + confidence) / 2, df=pooled_df)

    # results to data frame
    df = pd.DataFrame.from_dict(
        {
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
            "data_2": [x2_bar, s2_squared, n_2, "", "", "", "", "", "", "", ""],
        }
    ).set_index("t-test statistics")

    return df

def homo_variance_test(group1, group2, alpha=0.05):
    """
    Perform various tests to check the homogeneity of variance between two groups.

    This function conducts a series of tests to evaluate whether two groups have equal variances:
    1. Rule of thumb: Compares the ratio of the larger variance to the smaller variance.
    2. F-test: A parametric test that compares the variances of the two groups.
    3. Levene's test: A non-parametric test that checks the equality of variances.
    4. Bartlett's test: Another parametric test for homogeneity of variances, sensitive to normality assumptions.

    Args:
        group1 (array-like): The first group of data.
        group2 (array-like): The second group of data.
        alpha (float, optional): Significance level for the tests. Defaults to 0.05.

    Returns:
        pandas.DataFrame: A DataFrame containing the results of the tests.
    """
    s_1 = np.var(group1, ddof=1)
    s_2 = np.var(group2, ddof=1)

    s_max = max(s_1, s_2)
    s_min = min(s_1, s_2)
    f_ratio = s_max / s_min
    rot = f_ratio <= 4

    f_p_value = st.f_oneway(group1, group2)[1]
    l_p_value = st.levene(group1, group2)[1]
    b_p_value = st.bartlett(group1, group2)[1]

    d = {
        "Test": ["Rule of thumb", "F-test", "Levene's test", "Bartlett's test"],
        "Result": [
            "Variances are equal" if rot else "Variances are not equal",
            "Variances are equal" if f_p_value > alpha else "Variances are not equal",
            "Variances are equal" if l_p_value > alpha else "Variances are not equal",
            "Variances are equal" if b_p_value > alpha else "Variances are not equal",
        ],
        "Reasoning": [
            f"{s_max:.2f} / {s_min:.2f} = {f_ratio:.2f}",
            f"p value of F-test = {f_p_value:.8f}",
            f"p value of Levene's test = {l_p_value:.8f}",
            f"p value of Bartlett's test = {b_p_value:.8f}",
        ]
    }

    df_result = pd.DataFrame(d)
    return df_result