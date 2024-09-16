# __init__.py

from .descriptive import mean, median, cut_outliers
from .inferential import confidence_interval, t_test, homo_variance_test

__all__ = ['mean', 'median', 'cut_outliers', 'confidence_interval', 't_test', 'homo_variance_test']
__version__ = "0.1.0"