# coding: utf-8


### Generic data selection function


def get_data_selection(dataframe, selector_dict, selector_type='==', copy=True):
    """Return a dataframe containing data that matches all
       the criteria defined by `selector_dict`, which is a
       dictionary whose keys are the column name and values
       are the match criterion.
       Note that a copy of the original dataframe is made
       by default so any changes made to new data will not be
       reflected in the original data. 

       Input: Pandas dataframe, dictionary of selector values, selector type, 
              and copy

              selector_type is one of ['==' , '<', '>', '<=', '>=' ] and '=='
              is the default
              
              copy is True (default) or False and determines if a copy of the
              dataframe is made or not

       Output: Pandas dataframe for corresponding match
    """

    # Check selector_type
    if selector_type not in ['==', '<', '>', '<=', '>=']:
        raise SyntaxError("The selector_type must be a string and it must be one of the following: ['==', '<', '>', '<=', '>=']")

    # Make a copy of the original data
    if copy:
        table = dataframe.copy()
    else:
        table = dataframe

    # Select the data for each match criterion
    for key in selector_dict.keys():

        value = selector_dict[key]
        
        if key in table.index.names:
            selector_string = ' '.join(['table.index.get_level_values(key)', selector_type, 'value'])
        else:
            selector_string = ' '.join(['table[key]', selector_type, 'value'])

        table = table.ix[eval(selector_string)]

    # Clean up the index numbers if appropriate
    if copy and (None in table.index.names) and (len(table.index.names) == 1):
        table.reset_index(drop=True, inplace=True)

    return table
