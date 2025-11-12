# __init__.py

from .correlation import correlation_matrix, pearson_correlation, spearman_correlation
from .descriptive import cut_outliers, mean, median
from .inferential import confidence_interval, homo_variance_test, t_test

__all__ = [
    'mean',
    'median',
    'cut_outliers',
    'confidence_interval',
    't_test',
    'homo_variance_test',
    'pearson_correlation',
    'spearman_correlation',
    'correlation_matrix',
]
__version__ = "0.1.0"
