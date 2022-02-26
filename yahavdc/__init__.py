"""
Special module executed whenever the library is imported.
"""
from .parallelize import Distribute
from .consts import ADDITIONAL_RESULTS

__all__ = [Distribute, ADDITIONAL_RESULTS]
