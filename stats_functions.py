import math

import numpy as np
import pandas as pd
import scipy.stats as st

import re
import warnings

def clean_to_numeric_array(data):
    """
    Cleans up any data format (list, Series, set, generator) and returns a NumPy array
    of floats or integers. Handles common issues like missing values, invalid strings,
    whitespace, and other non-numeric data.

    Args:
        data (list, Series, set, generator): Input data that needs to be cleaned.

    Returns:
        np.ndarray: A cleaned NumPy array of numeric data (float or int).
    """
    # Convert data to an iterable list
    if isinstance(data, (pd.Series, list, set, tuple, np.ndarray)):
        data = list(data)
    elif hasattr(data, '__iter__'):
        data = list(data)
    else:
        raise ValueError("Unsupported data type. Provide list, Series, set, or generator.")

    # Helper function to clean individual values
    def clean_value(val):
        if pd.isna(val):  # Handle missing values (NaN, None)
            return np.nan
        
        if isinstance(val, str):
            # Remove extra whitespace
            val = val.strip()
            
            # Remove commas from numbers (e.g., "1,000" -> "1000")
            val = val.replace(',', '')

            # Remove any currency symbols or percentage signs
            val = re.sub(r'[^\d\.\-]', '', val)

            # Handle empty strings after cleaning
            if val == '':
                return np.nan

        # Attempt to convert cleaned value to a float
        try:
            return float(val)
        except ValueError:
            return np.nan  # Return NaN for any invalid conversions

    # Apply cleaning to the entire data array
    cleaned_data = np.array([clean_value(x) for x in data], dtype=float)

    # Optional: Filter out NaNs if desired (uncomment below to enable)
    cleaned_data = cleaned_data[~np.isnan(cleaned_data)]

    return cleaned_data 
    
    
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
    
    
def ci_variance(data, confidence=0.95):
    """
    Calculate the confidence interval (CI) for the population variance.
    
    The CI for population variance provides a range of values within which the true population variance is likely to lie, based on a sample. 
    Variance measures how spread out the data points are in the population.

    Args:
        data (array-like): The sample data for which to compute the confidence interval.
        confidence (float): The confidence level for the interval (e.g., 0.95 for 95% confidence).

    Returns:
        tuple: A tuple containing the lower and upper bounds of the confidence interval for the variance.
    
    Explanation:
        - The sample variance is calculated using Bessel's correction (ddof=1).
        - The confidence interval is computed using the chi-square distribution, which is appropriate for variance estimates.
        - The lower and upper bounds are based on the critical values from the chi-square distribution.
        
    Example:
        If `data` is a list of values and `confidence=0.95`, the function returns the 95% confidence interval for the variance.
    """
    data = clean_to_numeric_array(data)
    n = len(data)
    var = np.var(data, ddof=1)  # sample variance with Bessel's correction
    chi2_lower = st.chi2.ppf((1 - confidence) / 2, df=n - 1)  # (1 - 0.95)/2 = 0.025
    chi2_upper = st.chi2.ppf(
        (1 + confidence) / 2, df=n - 1
    )  # (1 + 0.95)/2 = 0.5 + 0.475 = 0.975
    lower = (n - 1) * var / chi2_upper
    upper = (n - 1) * var / chi2_lower
    return f"{confidence*100}% CI for population variance:", (float(lower), float(upper))

def ci_for_pop_proportion(p, n, confidence):
    """
    Calculate the confidence interval for a population proportion.
    

    Args:
        p (float): Sample proportion.
        n (int): Sample size.
        confidence (float): Desired confidence level (e.g., 0.95 for 95% confidence).

    Returns:
        tuple: A tuple containing the lower and upper bounds of the confidence interval.
    """
    standard_error = math.sqrt((p * (1 - p)) / n)

    # critical value for z alpha/2
    z = st.norm.ppf((1 + confidence) / 2)

    # confidence interval
    lower_bound = p - z * standard_error
    upper_bound = p + z * standard_error

    return f" {confidence*100}% CI for population proportion", (float(lower_bound), float(upper_bound))


def sample_size_for_pop_mean_ci(confidence, moe, pop_std):
    """
    Calculate the required sample size for a confidence interval that encloses
    the population mean with a given confidence and margin of error, assuming a normal distribution.

    Args:
        confidence (float): Desired confidence level (e.g., 0.95 for 95% confidence).
        moe (float): Desired margin of error.
        pop_std (float): Known population standard deviation.

    Returns:
        int: Required sample size (rounded up to the nearest integer).
    """
    z = st.norm.ppf((1 + confidence) / 2)
    sample_size = ((z * pop_std) / moe) ** 2
    return math.ceil(sample_size)


def sample_size_for_pop_proportion_ci(moe, confidence, p=0.5):
    """
    Calculate the required sample size for a population proportion confidence interval, 
    assuming a normal distribution.

    Parameters:
    ----------
        moe: float
            Desired margin of error as a proportion (e.g., 0.03 for 3%).
        confidence: float:
            Desired confidence level (e.g., 0.95 for 95%).
        p: float
            Estimated proportion of the population. Defaults to 0.5.

    Returns:
        int: Required sample size.
    """
    z = st.norm.ppf((1 + confidence) / 2)
    sample_size = ((z**2) * p * (1 - p)) / (moe**2)
    return math.ceil(sample_size)


def bootstrap(data, num_samples, statistic):
    """
    Perform bootstrap resampling to estimate a statistic.

    Args:
        data (array-like): The original sample data.
        num_samples (int): The number of bootstrap samples to generate.
        statistic (function): The statistic to estimate.

    Returns:
        ndarray: Array of bootstrap samples of the statistic.
    """
    bootstrap_samples_stat = []
    for _ in range(num_samples):
        sample = np.random.choice(data, len(data), replace=True)
        bootstrap_samples_stat.append(statistic(sample))
    return np.array(bootstrap_samples_stat)


def t_test_2sample( data_1, data_2, alpha=0.05, expected_diff=0, equal_var=True ):
    """_summary_

    Args:
        data_1 (_type_): _description_
        data_2 (_type_): _description_
        alpha (float, optional): _description_. Defaults to 0.05.
        expected_diff (int, optional): _description_. Defaults to 0.
        equal_var (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    confidence = 1 - alpha
    x1_bar = data_1.mean()
    x2_bar = data_2.mean()
    n_1 = int(len(data_1))
    n_2 = int(len(data_2))
    pooled_df = n_1 + n_2 - 2
    s1_squared = np.var(data_1, ddof=1)
    s2_squared = np.var(data_2, ddof=1)

    if equal_var:
        # t-statistic for equal variance
        numerator = x1_bar - x2_bar - expected_diff
        pooled_variance = ((n_1 - 1) * s1_squared + (n_2 - 1) * s2_squared) / (
            pooled_df
        )
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


def ttest_paired_2sample(data_1, data_2, alpha=0.05, expected_diff=0):

    confidence = 1- alpha
    x1_bar = data_1.mean()
    x2_bar = data_2.mean()
    n_1 = len(data_1)
    n_2 = len(data_2)
    var_1 = np.var(data_1, ddof=1)
    var_2 = np.var(data_2, ddof=1)
    d = data_1 - data_2 
    d_bar = d.mean()
    n = len(d)
    df = n-1
    var = np.var(d, ddof=1)
    t_statistic = (d_bar - expected_diff)/np.sqrt(var/n)
    p_one_tail = 1 - st.t.cdf(abs(t_statistic), df)
    t_critical_one_tail = st.t.ppf(confidence, df=df)
    p_two_tail = 2 * (1 - st.t.cdf(abs(t_statistic), df))
    t_critical_two_tail = st.t.ppf((1 + confidence) / 2, df=df)
    pearson_corr = np.corrcoef(data_1, data_2)[0, 1]

    df = pd.DataFrame.from_dict(
        {
            "t-test statistics": [
                "Mean",
                "Variance",
                "Observations",
                "Pearson Correlation Coefficient",
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
                var_1,
                n_1,
                pearson_corr,
                expected_diff,
                df,
                t_statistic,
                p_one_tail,
                t_critical_one_tail,
                p_two_tail,
                t_critical_two_tail,
            ],
            "data_2": [x2_bar, var_2, n_2, "", "", "", "", "", "", "", ""],
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
        dict: A dictionary containing the results of the tests, including:
            - "Test": Names of the tests performed.
            - "Result": Conclusion of each test (whether variances are equal or not).
            - "Reasoning": Explanation for each conclusion, including the test statistic or p-value.
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


def cut_outliers(df, col, method='q'):
    """Removes outliers from a DataFrame based on a specified column.

    This function identifies outliers using either the interquartile range (IQR) method
    or z-scores. 
    
    Any data points falling below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are
    considered outliers in the IQR method. 
    
    For the z-score method, any data points with
    z-scores outside the range [-3, 3] are considered outliers.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str): The column name for which outliers are to be removed.
        method (str, optional): The method to use for outlier removal. Options are 'q' for
            IQR method (default) or 'z' for z-score method.

    Returns:
        pd.DataFrame: A DataFrame with outliers removed from the specified column.

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 100]})
        >>> df_cleaned = cut_outliers(df, 'A', method='z')
    """
    if method == 'q':
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        return df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]

    elif method == 'z':
        z_scores = (df[col] - df[col].mean()) / df[col].std()
        return df[abs(z_scores) <= 3]

    else:
        raise ValueError("Invalid method. Use 'q' for IQR method or 'z' for z-score method.")






