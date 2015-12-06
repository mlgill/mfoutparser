# coding: utf-8
__all__ = ["parse_mfout", "write_all_to_file", "write_correlation_matrix_to_file",
           "make_correlation_matrices", "get_data_selection"]
           
from .read import parse_mfout
from .write import write_all_to_file, write_correlation_matrix_to_file
from .correlation import make_correlation_matrices
from .selector import get_data_selection

from .docstring import DOCSTRING
from .version import VERSION

__doc__ = DOCSTRING
__version__ = VERSION

