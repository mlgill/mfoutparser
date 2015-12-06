# coding: utf-8


### Generic data selection function


def get_data_selection(dataframe, selector_dict, copy=True):
    """Return a dataframe containing data that matches all
       the criteria defined by `selector_dict`, which is a
       dictionary whose keys are the column name and values
       are the match criterion.
       Note that a copy of the original dataframe is made
       by default so any changes made to new data will not be
       reflected in the original data. 
       Input: Pandas dataframe, dictionary of selector values, and copy (True/False)
       Output: Pandas dataframe for corresponding match
    """

    # Make a copy of the original data
    if copy:
        table = dataframe.copy()
    else:
        table = dataframe

    # Select the data for each match criterion
    for key in selector_dict.keys():

        value = selector_dict[key]

        if key in table.index.names:
            table = table.ix[table.index.get_level_values(key) == value]
        else:
            table = table.ix[table[key] == value]

    # Clean up the index numbers if appropriate
    if copy and (None in table.index.names) and (len(table.index.names) == 1):
        table.reset_index(drop=True, inplace=True)

    return table
