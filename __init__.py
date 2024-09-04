# __init__.py

from .descriptive import mean, median  # Assuming these functions are defined in descriptive.py
from .inferential import t_test  # Assuming this function is defined in inferential.py

__all__ = ['mean', 'median', 't_test']
