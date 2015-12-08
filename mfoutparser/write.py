# coding: utf-8


### Export data to file


def _write_tag_loop_dict_to_file(tag_loop_dict, filename_prefix=u'', preserve_format=True, 
                                 sep='\t', na_rep=u'', index=True, *args, **kwargs):
    """Write a tag or loop dictionary to a file
       This is a private function, not meant for general use.

       Input: dictionary of dataframes, prefix for file name

       Output: tab-separated file for each dictionary
    """

    extension = '.tsv'
    
    # Write all the dataframes to separate files with the key name appended
    for key in tag_loop_dict.keys():

        # Make the filename
        if filename_prefix is u'':
            filename = key
        else:
            filename = u'_'.join([filename_prefix, key])

        filename += extension

        dataframe = tag_loop_dict[key]

        dataframe.to_csv(filename, preserve_format=preserve_format, 
                         sep=sep, na_rep=na_rep, index=index, *args, **kwargs)
        
    return


def write_all_to_file(tag_dict, loop_dict, filename_prefix=u'', preserve_format=True, 
                      sep='\t', na_rep=u'', index=True, *args, **kwargs):
    """Write ModelFree parsed data to tab-separated files

       Input: dictionaries created by parse_mfout and optional
              filename prefix

       Output: tab-separated files
    """
    
    # Write all the tables in both the tag and 
    # loop dictionaries to a file
    
    tag_prefix = u'tag'
    loop_prefix = u'loop'
    
    if filename_prefix is not '':
        tag_prefix = u'_'.join([filename_prefix, tag_prefix])
        loop_prefix = u'_'.join([filename_prefix, loop_prefix])
        
    _write_tag_loop_dict_to_file(tag_dict, tag_prefix, preserve_format=preserve_format, 
                                 sep=sep, na_rep=na_rep, index=index, *args, **kwargs)
    _write_tag_loop_dict_to_file(loop_dict, loop_prefix, preserve_format=preserve_format, 
                                 sep=sep, na_rep=na_rep, index=index, *args, **kwargs)
    
    return


def write_correlation_matrix_to_file(dataframe, filename_prefix=u'', preserve_format=True, 
                                    sep='\t', na_rep=u'', index=True, *args, **kwargs):
    """Write pivoted correlation matrix to file

       Input: dataframe created by `make_correlation_matrices`, optional
              filename prefix, and the value to use for undefined entries 
              (left empty by default)

       Output: tab-separated file named with `filename_prefix` 
               and 'correlation_matrix_pivot'
    """

    extension='.tsv'

    filename = u'correlation_matrix_pivot'
    if filename_prefix is not '':
        filename = '_'.join([filename_prefix, filename])

    filename += extension

    dataframe.to_csv(filename, preserve_format=preserve_format, 
                     sep=sep, na_rep=na_rep, index=index, *args, **kwargs)

    return


