# coding: utf-8
from .read import DataFrame


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
    correlation_matrix = DataFrame(correlation_matrix)

    # Pandas groupby doesn't preserve the print formatter
    correlation_matrix = correlation_matrix.__finalize__(dataframe, 'copy')

    # Append columns for each of the parameters in 'model_free_name_2'
    new_col_names = dataframe.model_free_name_2.unique()

    for col in new_col_names:
        correlation_matrix._print_format[col] = correlation_matrix._print_format['covariance']

    return correlation_matrix

