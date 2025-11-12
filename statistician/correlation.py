"""
Correlation analysis functions.

This module provides functions for calculating correlation coefficients
between two variables, including Pearson and Spearman correlations.
"""

import numpy as np
import pandas as pd
import scipy.stats as st

from .descriptive import clean_to_numeric_array


def pearson_correlation(x, y, alpha=0.05):
    """
    Calculate Pearson correlation coefficient between two variables.

    Pearson correlation measures the linear relationship between two continuous
    variables. The coefficient ranges from -1 (perfect negative correlation) to
    +1 (perfect positive correlation), with 0 indicating no linear correlation.

    Assumptions:
    - Both variables are continuous
    - Linear relationship between variables
    - Bivariate normal distribution (for significance testing)
    - No significant outliers

    Args:
        x (array-like): First variable (continuous data)
        y (array-like): Second variable (continuous data)
        alpha (float, optional): Significance level for hypothesis test.
                                Defaults to 0.05.

    Returns:
        pandas.DataFrame: DataFrame containing:
            - Correlation Coefficient (r): Pearson correlation coefficient
            - P-value: Two-tailed p-value for hypothesis test
            - Significant: Whether correlation is significant at alpha level
            - Sample Size: Number of paired observations
            - Confidence Interval: 95% confidence interval for r

    Raises:
        ValueError: If x and y have different lengths, are empty, have fewer
                   than 2 observations, or alpha is not between 0 and 1.

    Example:
        >>> x = [1, 2, 3, 4, 5]
        >>> y = [2, 4, 5, 4, 5]
        >>> result = pearson_correlation(x, y)
        >>> print(result)
        >>> print(f"Correlation: {result.loc[0, 'Correlation Coefficient (r)']:.3f}")

    Note:
        Pearson correlation only measures linear relationships. For non-linear
        relationships or ordinal data, consider Spearman correlation.
    """
    # Validate alpha
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")

    # Clean and validate input data
    x_clean = clean_to_numeric_array(x)
    y_clean = clean_to_numeric_array(y)

    # Check for empty arrays
    if len(x_clean) == 0 or len(y_clean) == 0:
        raise ValueError("Input arrays cannot be empty")

    # Check equal lengths
    if len(x_clean) != len(y_clean):
        raise ValueError(
            f"x and y must have the same length. Got x: {len(x_clean)}, y: {len(y_clean)}"
        )

    # Check minimum sample size
    if len(x_clean) < 2:
        raise ValueError("At least 2 paired observations are required")

    n = len(x_clean)

    # Calculate Pearson correlation coefficient and p-value
    r, p_value = st.pearsonr(x_clean, y_clean)

    # Check for significance
    significant = p_value < alpha

    # Calculate confidence interval for r using Fisher's Z transformation
    # Z = 0.5 * ln((1 + r) / (1 - r))
    if abs(r) < 0.9999:  # Avoid division by zero for r very close to ±1
        z = 0.5 * np.log((1 + r) / (1 - r))
        se_z = 1 / np.sqrt(n - 3)
        z_critical = st.norm.ppf(1 - alpha / 2)

        z_lower = z - z_critical * se_z
        z_upper = z + z_critical * se_z

        # Transform back to r scale
        r_lower = (np.exp(2 * z_lower) - 1) / (np.exp(2 * z_lower) + 1)
        r_upper = (np.exp(2 * z_upper) - 1) / (np.exp(2 * z_upper) + 1)

        ci = f"({r_lower:.3f}, {r_upper:.3f})"
    else:
        ci = "N/A (r too close to ±1)"

    # Determine correlation strength
    abs_r = abs(r)
    if abs_r < 0.3:
        strength = "Weak"
    elif abs_r < 0.7:
        strength = "Moderate"
    else:
        strength = "Strong"

    # Determine direction
    direction = "Positive" if r > 0 else "Negative" if r < 0 else "None"

    # Create results DataFrame
    results = pd.DataFrame({
        'Statistic': [
            'Correlation Coefficient (r)',
            'P-value',
            f'Significant (α={alpha})',
            'Sample Size',
            f'{int((1-alpha)*100)}% Confidence Interval',
            'Strength',
            'Direction'
        ],
        'Value': [
            f"{r:.6f}",
            f"{p_value:.6f}",
            str(significant),
            str(n),
            ci,
            strength,
            direction
        ]
    })

    return results


def spearman_correlation(x, y, alpha=0.05):
    """
    Calculate Spearman rank correlation coefficient between two variables.

    Spearman correlation measures the monotonic relationship between two
    variables using ranked values. It's more robust to outliers and doesn't
    assume a linear relationship or normal distribution.

    Use Spearman when:
    - Data is ordinal (ranked)
    - Relationship is non-linear but monotonic
    - Data contains outliers
    - Assumptions for Pearson correlation are violated

    Args:
        x (array-like): First variable
        y (array-like): Second variable
        alpha (float, optional): Significance level. Defaults to 0.05.

    Returns:
        pandas.DataFrame: DataFrame containing:
            - Correlation Coefficient (ρ): Spearman's rho
            - P-value: Two-tailed p-value
            - Significant: Whether correlation is significant
            - Sample Size: Number of paired observations

    Raises:
        ValueError: If x and y have different lengths, are empty, have fewer
                   than 2 observations, or alpha is not between 0 and 1.

    Example:
        >>> x = [1, 2, 3, 4, 5]
        >>> y = [1, 4, 9, 16, 25]  # Non-linear but monotonic
        >>> result = spearman_correlation(x, y)
        >>> print(result)

    Note:
        Spearman correlation is equivalent to Pearson correlation on ranked data.
        It detects monotonic relationships (consistently increasing or decreasing),
        not just linear relationships.
    """
    # Validate alpha
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")

    # Clean and validate input data
    x_clean = clean_to_numeric_array(x)
    y_clean = clean_to_numeric_array(y)

    # Check for empty arrays
    if len(x_clean) == 0 or len(y_clean) == 0:
        raise ValueError("Input arrays cannot be empty")

    # Check equal lengths
    if len(x_clean) != len(y_clean):
        raise ValueError(
            f"x and y must have the same length. Got x: {len(x_clean)}, y: {len(y_clean)}"
        )

    # Check minimum sample size
    if len(x_clean) < 2:
        raise ValueError("At least 2 paired observations are required")

    n = len(x_clean)

    # Calculate Spearman correlation coefficient and p-value
    rho, p_value = st.spearmanr(x_clean, y_clean)

    # Check for significance
    significant = p_value < alpha

    # Determine correlation strength
    abs_rho = abs(rho)
    if abs_rho < 0.3:
        strength = "Weak"
    elif abs_rho < 0.7:
        strength = "Moderate"
    else:
        strength = "Strong"

    # Determine direction
    direction = "Positive" if rho > 0 else "Negative" if rho < 0 else "None"

    # Create results DataFrame
    results = pd.DataFrame({
        'Statistic': [
            'Correlation Coefficient (ρ)',
            'P-value',
            f'Significant (α={alpha})',
            'Sample Size',
            'Strength',
            'Direction'
        ],
        'Value': [
            f"{rho:.6f}",
            f"{p_value:.6f}",
            str(significant),
            str(n),
            strength,
            direction
        ]
    })

    return results


def correlation_matrix(data, method='pearson', alpha=0.05):
    """
    Calculate correlation matrix for multiple variables.

    Computes pairwise correlations between all columns in a DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with numeric columns
        method (str, optional): Correlation method - 'pearson' or 'spearman'.
                               Defaults to 'pearson'.
        alpha (float, optional): Significance level. Defaults to 0.05.

    Returns:
        tuple: (correlation_matrix, p_value_matrix)
            - correlation_matrix: DataFrame with correlation coefficients
            - p_value_matrix: DataFrame with corresponding p-values

    Raises:
        ValueError: If method is invalid, data is not a DataFrame, or
                   data contains non-numeric columns.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'height': [170, 175, 180, 165, 172],
        ...     'weight': [65, 72, 78, 60, 68],
        ...     'age': [25, 30, 35, 22, 28]
        ... })
        >>> corr_matrix, p_matrix = correlation_matrix(df)
        >>> print(corr_matrix)
    """
    # Validate inputs
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Data must be a pandas DataFrame")

    if method not in ['pearson', 'spearman']:
        raise ValueError("Method must be 'pearson' or 'spearman'")

    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.empty:
        raise ValueError("DataFrame must contain at least one numeric column")

    if len(numeric_data.columns) < 2:
        raise ValueError("DataFrame must contain at least 2 numeric columns")

    n_vars = len(numeric_data.columns)

    # Initialize matrices
    corr_matrix = pd.DataFrame(
        np.zeros((n_vars, n_vars)),
        index=numeric_data.columns,
        columns=numeric_data.columns
    )

    p_matrix = pd.DataFrame(
        np.zeros((n_vars, n_vars)),
        index=numeric_data.columns,
        columns=numeric_data.columns
    )

    # Calculate pairwise correlations
    for i, col1 in enumerate(numeric_data.columns):
        for j, col2 in enumerate(numeric_data.columns):
            if i == j:
                # Correlation of variable with itself is 1
                corr_matrix.iloc[i, j] = 1.0
                p_matrix.iloc[i, j] = 0.0
            else:
                # Calculate correlation
                x = numeric_data[col1].dropna()
                y = numeric_data[col2].dropna()

                # Find common indices (in case of missing values)
                common_idx = numeric_data[[col1, col2]].dropna().index
                x = numeric_data.loc[common_idx, col1]
                y = numeric_data.loc[common_idx, col2]

                if len(x) >= 2:
                    if method == 'pearson':
                        r, p = st.pearsonr(x, y)
                    else:  # spearman
                        r, p = st.spearmanr(x, y)

                    corr_matrix.iloc[i, j] = r
                    p_matrix.iloc[i, j] = p
                else:
                    corr_matrix.iloc[i, j] = np.nan
                    p_matrix.iloc[i, j] = np.nan

    return corr_matrix, p_matrix
