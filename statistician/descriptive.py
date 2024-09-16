import numpy as np
import pandas as pd
import re

def clean_to_numeric_array(data):
    """
    Cleans input data to return a NumPy array of floats or integers. Handles
    various dirty data issues like missing values, invalid strings, whitespace,
    currency symbols, percentage signs, and more.

    Args:
        data (list, Series, set, generator): Input data to be cleaned.

    Returns:
        np.ndarray: A cleaned NumPy array of numeric data (float or int).
    """
    if isinstance(data, (pd.Series, list, set, tuple, np.ndarray)):
        data = np.array(data)
    elif hasattr(data, '__iter__'):
        data = np.array(list(data))
    else:
        raise ValueError("Unsupported data type. Provide list, Series, set, or generator.")
    
    # Define a vectorized clean function
    def clean_value_vectorized(values):
        # Initialize a mask for NaN
        cleaned_values = np.empty(values.shape, dtype=object)
        cleaned_values[:] = np.nan  # Default all to NaN

        # Regex patterns to clean the data
        numeric_pattern = re.compile(r'^-?\d+(\.\d+)?$')  # Matches valid integers and floats
        special_characters_pattern = re.compile(r'[^\d\.\-]')

        for i, val in enumerate(values):
            if pd.isna(val):  # Handle missing values directly
                continue
            
            if isinstance(val, str):
                # Clean the string
                val = val.strip()
                val = val.replace(',', '')  # Remove commas
                
                # Remove unwanted characters
                val = special_characters_pattern.sub('', val)
                
                # If the cleaned string is empty, remains NaN
                if val == '':
                    continue
            
            try:
                # Attempt to convert to float
                cleaned_values[i] = float(val)
            except ValueError:
                cleaned_values[i] = np.nan  # Invalid conversion

        return cleaned_values

    # Clean the data and convert to a NumPy array
    cleaned_data = clean_value_vectorized(data)

    # Optionally filter out NaNs
    cleaned_data = cleaned_data[~pd.isna(cleaned_data)]

    return cleaned_data.astype(float)  # Ensure output is float type

def mean(data):
    """
    Calculate the arithmetic mean of the data.

    Args:
        data (array-like): Input data.

    Returns:
        float: The arithmetic mean of the data.
    """
    clean_data = clean_to_numeric_array(data)
    return np.mean(clean_data)

def median(data):
    """
    Calculate the median of the data.

    Args:
        data (array-like): Input data.

    Returns:
        float: The median of the data.
    """
    clean_data = clean_to_numeric_array(data)
    return np.median(clean_data)

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