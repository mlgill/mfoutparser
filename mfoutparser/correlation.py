# coding: utf-8
from .read import _DataFrame_mf


### A function to handle creation and display of the correlation matrix


def make_correlation_matrices(dataframe):
    """Convert a dataframe of correlation data into a matrix

       Input: Pandas dataframe containing correlation data

       Output: Pandas dataframe with data manipulated into matrices
    """

    # Group the data by residue then use a pivot table-like function
    # to create correlation matrices
    if u'residue' in dataframe.index.names:
        correlation_group = dataframe.reset_index().groupby(u'residue')
    else:
        correlation_group = dataframe.groupby(u'residue')

    correlation_matrix = correlation_group.apply(lambda x: x.pivot(index=u'model_free_name_1', 
                                                                   columns=u'model_free_name_2', 
                                                                   values=u'covariance'))
    return _DataFrame_mf(correlation_matrix)

