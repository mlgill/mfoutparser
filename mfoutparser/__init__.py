# coding: utf-8
__all__ = [u"parse_mfout", u"write_all_to_file", u"write_correlation_matrix_to_file",
           u"make_correlation_matrices", u"get_data_selection"]
           
from .read import parse_mfout
from .write import write_all_to_file, write_correlation_matrix_to_file
from .correlation import make_correlation_matrices
from .selector import get_data_selection

from .docstring import DOCSTRING
from .version import VERSION

DOCSTRING = DOCSTRING + u'\n' + \
            u'See the `examples` directory in {:s} for a demonstration.'.format(__path__[0])

__doc__ = DOCSTRING
__version__ = VERSION

