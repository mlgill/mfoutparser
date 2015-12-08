# coding: utf-8
__all__ = [u"parse_mfout", u"write_all_to_file", u"write_correlation_matrix_to_file",
           u"make_correlation_matrices", u"get_data_selection", u"copy_examples"]


from .read import parse_mfout, DataFrame
from .write import write_all_to_file, write_correlation_matrix_to_file
from .correlation import make_correlation_matrices
from .selector import get_data_selection
from .examples import copy_examples

from .docstring import DOCSTRING
from .version import VERSION

# TODO find a way to fix the docstring indentation for classes
__doc__ = '\n'.join([DOCSTRING, 'CLASSES', DataFrame.__doc__])
__version__ = VERSION
