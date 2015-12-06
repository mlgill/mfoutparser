# coding: utf-8


### Export data to file


def _write_dataframe_to_file(dataframe, filename, na_rep=u'', extension=u'.tsv'):
    """Write a single dataframe to a file
       This is a private function, not meant for general use.

       Input: dataframe, prefix for file name

       Output: tab-separated file
    """

    # Add extension to the output filename
    filename += extension

    # Determine if the index should be saved--only want to save if it 
    # includes actual data
    save_index = True
    if ((None in dataframe.index.names) and (len(dataframe.index.names) == 1)):
        save_index = False

    # Function to format significant digits on floats
    format_dict = dataframe._print_format
    dataframe = dataframe.copy()
    for key in format_dict.keys():
        format_string = format_dict[key]
        dataframe[key] = dataframe[key].apply(lambda x: format_string.format(x))

    # Write the table to a file
    dataframe.to_csv(filename, sep='\t', na_rep=na_rep, index=save_index)

    return


def _write_tag_loop_dict_to_file(tag_loop_dict, filename_prefix):
    """Write a tag or loop structure to a file
       This is a private function, not meant for general use.

       Input: dictionary of dataframes, prefix for file name

       Output: tab-separated file for each dictionary
    """
    
    # Write all the dataframes to separate files with the key name appended
    for key in tag_loop_dict.keys():

        # Make the filename
        if filename_prefix is u'':
            filename = key
        else:
            filename = u'_'.join([filename_prefix, key])

        _write_dataframe_to_file(tag_loop_dict[key], filename=filename)
        
    return


def write_all_to_file(tag_dict, loop_dict, filename_prefix=u''):
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
        
    _write_tag_loop_dict_to_file(tag_dict, tag_prefix)
    _write_tag_loop_dict_to_file(loop_dict, loop_prefix)
    
    return


def write_correlation_matrix_to_file(dataframe, filename_prefix=u'', na_rep=u''):
    """Write pivoted correlation matrix to file

       Input: dataframe created by `make_correlation_matrices`, optional
              filename prefix, and the value to use for undefined entries 
              (left empty by default)

       Output: tab-separated file named with `filename_prefix` 
               and 'correlation_matrix_pivot'
    """

    filename = u'correlation_matrix_pivot'
    if filename_prefix is not '':
        filename = '_'.join([filename_prefix, filename])

    _write_dataframe_to_file(dataframe, filename=filename, na_rep=na_rep)

    return



