# coding: utf-8
import re
import sys
import pandas as pd
from pandas import DataFrame as pd_DataFrame
import numpy as np
from collections import OrderedDict

### A custom class to handle display and formatting of data during output


class DataFrame(pd_DataFrame):
    """`mfoutparser` creates a custom dataframe class, called DataFrame, that is essentially
       identical to (and based on) Pandas dataframe, with the following minor changes:

       1. The function used to display the dataframe in the html IPython notebook 
       will filter out the NaN values before displaying the table. It is important to 
       leave the NaN values in place in the underlying table for mathematical manipulation.

       2. This dataframe also contains a custom attribute called '_print_format' that 
       contains a dictionary whose keys correspond to the original format 
       (decimal places) of float columns when read from the Model-Free output files. 
       This dictionary can be used to ensure the correct float format is preserved when
       writing the data to tab delimited files.

       Type 'help(mf.DataFrame)' for more information.
    """

    # TODO check that docstrigns are correct for the over written methods

    @property
    def _constructor(self):
        return DataFrame


    def __init__(self, *args, **kwargs):
        # Initialize the dataframe as Pandas would and 
        # then also add a _print_format property
        super(DataFrame, self).__init__(*args, **kwargs)

        # Create print formatter and append to method list which helps with propagation
        self._print_format = dict()
        if '_print_format' not in self._metadata:
            self._metadata.append('_print_format')

        return


    def __finalize__(self, other, method=None, **kwargs):
        # propagate metadata from other to self
        # other : the object from which to get the attributes that we are going to propagate
        # method : optional, a passed method name, usually set to 'copy' if used

        if isinstance(other, pd.core.generic.NDFrame):
            for name in self._metadata:
                if method is None:
                    object.__setattr__(self, name, getattr(other, name, None))
                elif method is 'copy':
                    object.__setattr__(self, name, getattr(other, name, None).copy())

        return self


    def _repr_html_(self):
        # Replace all NaN values with '' and then 
        # run the Pandas dataframe html representation function
        return super(DataFrame, self.replace(to_replace=u'NaN', value=''))._repr_html_()


    def copy(self):
        # Ensure the _print_format property is duplicated when making a copy
        return super(DataFrame, self).copy().__finalize__(self, 'copy')


    def to_csv(self, filename, preserve_format=True, 
               sep='\t', na_rep=u'', index=None, *args, **kwargs):

        # If the index has not been set to True or False (which determines
        # if it should be written, then try to guess
        # We only want to save if it includes actual data
        if index is None:
            index = True
            if ((None in self.index.names) and (len(self.index.names) == 1)):
                index = False


        # Function to format significant digits on floats by converting them to strings
        if ( preserve_format and hasattr(self, '_print_format') ):

            format_dict = self._print_format.copy()
            dataframe = self.copy()

            # Move the index to the dataframe if it should be saved
            if index:
                dataframe = dataframe.reset_index()
                index = False

            # If NaN replacement is a number, replace before converting to string
            if ( isinstance(na_rep, int) or isinstance(na_rep, float) ):
                dataframe = dataframe.replace(np.NaN, na_rep)

            for key in format_dict.keys():
                format_string = format_dict[key]

                if key in dataframe.columns:
                    dataframe[key] = dataframe[key].apply(lambda x: format_string.format(x))

            # If NaN replacement is a string, replace after converting to string
            # General string class is different in Python 2 and 3....
            if sys.version_info[0] == 2:
                if isinstance(na_rep, basestring):
                    dataframe = dataframe.replace(r"""[Nn][Aa][Nn]""", na_rep, regex=True)
            elif sys.version_info[0] >= 3:
                if isinstance(na_rep, str):
                    dataframe = dataframe.replace(r"""[Nn][Aa][Nn]""", na_rep, regex=True)

        else:
            # Otherwise just use default formatting
            dataframe = self

        # Call Pandas to_csv function
        super(DataFrame, dataframe).to_csv(filename, sep=sep, na_rep=na_rep, index=index,
                                           *args, **kwargs)

        return


### The primary parsing function


def parse_mfout(mfoutfilename):
    """Parse a ModelFree output file

       Input: path to ModelFree output file

       Output: two dictionaries containing data
               and tables. The tables are dataframes,
               as created by Pandas.
    """
    
    tag_data_dict = _parse_mfoutfile(mfoutfilename)

    tag_dict = OrderedDict()
    loop_dict = OrderedDict()

    for key in tag_data_dict.keys():
        text_list = tag_data_dict[key]
        text_loops, text_tags = _split_loop_and_tag_text(text_list)

        # Aggregate all of the data that aren't loops
        if len(text_tags) > 0:
            text_dict_tags = _convert_tags_to_dict(text_tags)
            text_df_tags = _convert_tags_to_df(text_dict_tags)
            tag_dict[key] = text_df_tags

        # Aggregate the loops    
        if len(text_loops) > 0:
            text_df_loops = _convert_loops_to_df(text_loops)
            loop_dict[key] = text_df_loops
            
    # Clean up the data_header tag in loop_dict
    # which sometimes has multiple entries
    loop_dict = _clean_up_loop_dict(loop_dict)
        
    # Clean up the tag names in tag_dict and
    # the column names in the loop_dict
    tag_dict = _clean_up_tag_dict_tags(tag_dict)
    loop_dict = _clean_up_table_column_names(loop_dict)

    # Coerce column types to integers and numeric when possible
    tag_dict = _coerce_and_store_data_types(tag_dict)
    loop_dict = _coerce_and_store_data_types(loop_dict)

    # Remove the 'data_' portion of the key name since it's unnecessary
    for _ in range(len(tag_dict)):
        key, value = tag_dict.popitem(False)
        tag_dict[key.replace(u'data_', u'')] = value

    for _ in range(len(loop_dict)):
        key, value = loop_dict.popitem(False)
        loop_dict[key.replace(u'data_', u'')] = value
            
    return tag_dict, loop_dict


### Initial string parsing function


def _parse_mfoutfile(mfoutfilename):
    """Read in the file and split the data tags into a dictionary.
       This is a private function, not meant for general use.

       Input: path to ModelFree file

       Output: a dictionary with unparsed data
    """
    
    # Read the file
    file_string = open(mfoutfilename, 'r').read()

    # Remove any Windows linefeed characters (courtesy of Microsoft Exchange/Outlook)
    regex_microsoftsucks = re.compile(r"""\r\n""")
    file_string = re.sub(regex_microsoftsucks, '\n', file_string)
    
    # Remove comments from the text
    regex_comment = re.compile(r"""(^\s?#.+|^\s?)\n""")
    file_string = re.sub(regex_comment, '', file_string)
    
    # Remove internal double returns from the data
    regex_returns = re.compile(r"""\n{2,}""")
    file_string = re.sub(regex_returns, '\n', file_string)
    
    # Strip whitespace from the beginning and end of the data
    file_string = file_string.strip()

    # Split the data into a list based on the data_x tags
    regex_data_tag_split = re.compile(r"""\n(?=data_.+?\n)""")
    split_list = re.split(r"""\n(?=data_.+?\n)""", file_string, flags=re.MULTILINE|re.DOTALL)
    
    # Separate the data tags from the corresponding data
    regex_data_tag_name = re.compile(r"""(data_.+?)\n(.+)""")
    tag_data_list = [re.search(r"""(data_.+?)\n(.+)""", x, flags=re.MULTILINE|re.DOTALL) 
                     for x in split_list]
    
    # Put the list into an ordered dictionary with the tag as a key
    tag_data_dict = OrderedDict([(x.group(1).strip(), x.group(2)) 
                                  for x in tag_data_list])
    
    return tag_data_dict


### Split string into loop and tag data


def _split_loop_and_tag_text(text_list):
    """Split the text corresponding to a single label and create table.
       This is a private function, not meant for general use.

       Input: data for a single tab

       Output: dataframes corresponding to single data and tables
    """

    # Split into separate lines and put into a
    # pandas dataframe so data selection is easier
    text_list = text_list.split('\n')
    text_df = pd.DataFrame(text_list, columns=[u'text'])
    
    # Strip the whitespace off the beginning and end
    text_df[u'text'] = text_df.text.str.strip()
    
    # This column determines if text contains a _tag
    text_df[u'tag'] = False
    text_df.ix[text_df.text.str.contains('_\w+',regex=True),u'tag'] = True

    # This column determines if text contains a loop tag (loop_)
    text_df[u'loop'] = False
    text_df.ix[text_df.text.str.contains('loop_'),u'loop'] = True
    
    # The line below the tag is always part of the tag group
    text_df.ix[text_df.ix[text_df.loop].index+1, u'loop'] = True

    # Any row that doesn't contain a tag and is not currently part of a loop
    # must also be part of a loop
    text_df.ix[(text_df.tag==False)&(text_df.loop!=True),u'loop'] = True
    
    # Separate the data that is not part of a loop
    text_df_tags = text_df.ix[text_df.loop==False, u'text'].tolist()
    
    # Separate the data that is part of a loop
    text_df_loop = text_df.ix[text_df.loop==True, u'text'].tolist()

    return text_df_loop, text_df_tags


### Convert the tag data to a ModelFree DataFrame


def _convert_tags_to_dict(text_list_tags):
    """Convert all tag data to a dictionary
       This is a private function, not meant for general use.

       Input: list of text tags

       Output: dictionary
    """
    return OrderedDict([re.findall(r"""\s*_(\w+)\s+(.+?)\s*$""", row)[0] for row in text_list_tags])


def _convert_tags_to_df(text_dict_tags):
    """Convert all dictionary data to a dataframe
       This is a private function, not meant for general use.

       Input: dictionary

       Output: dataframe
    """

    return DataFrame({u'tag'  :[item[0] for item in text_dict_tags.items()],
                      u'value':[item[1] for item in text_dict_tags.items()]})


def _clean_up_tag_dict_tags(tag_dict):
    """Clean up tag names in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # Make the tag label all lowercase
    # and remove any underscores from the beginning
    for key in tag_dict.keys():
        tag_dict[key][u'tag'] = tag_dict[key][u'tag'].str.lower()
        tag_dict[key][u'tag'].replace(r"""^_""", u'', inplace=True, regex=True)
        
    return tag_dict


### Convert the loop data to a _DataFrame_mf


def _set_loops(loop_data):
    """Find limits of loops in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    # Initiate a loop column with 1 for each loop tag
    loop_data[u'loop'] = 0
    loop_data.ix[loop_data.text.str.contains(u'loop_'),u'loop'] = 1

    # Ensure the index is linear, but set it up so the original
    # index can be replaced
    old_columns = loop_data.columns
    loop_data = loop_data.reset_index(drop=False)
    index_column = list(set(loop_data.columns) - set(old_columns))
    
    # Get the difference between index positions of the loop tags
    loop_index = loop_data.ix[loop_data.loop==1].index
    loop_diff = loop_index[1:] - loop_index[:-1]

    # For nested loops, the difference 
    depth = 0
    for idx,diff in zip(loop_index[:-1],loop_diff):
        if diff <= 2:
            depth += 1
            loop_data.ix[idx,u'loop'] += depth
        else:
            depth = 0
            
    
    # Reset the index
    loop_data.set_index(index_column, drop=True)
    if u'index' in loop_data.columns:
        loop_data = loop_data.drop([u'index'], axis = 1)
    
    return loop_data


def _set_labels(loop_data):
    """Find labels in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # Ensure the index is linear, but set it up so the original
    # index can be replaced
    old_columns = loop_data.columns
    loop_data = loop_data.reset_index(drop=False)
    index_column = list(set(loop_data.columns) - set(old_columns))
    
    # The non-zero values of the loops and their new index
    tag_values = loop_data.ix[loop_data.loop !=0,u'loop'].tolist()
    tag_index = loop_data.ix[loop_data.loop !=0].index + 1

    loop_data[u'tag'] = 0
    loop_data.ix[tag_index, u'tag'] = tag_values
    
    # Reset the index
    loop_data.set_index(index_column, drop=True)
    if u'index' in loop_data.columns:
        loop_data = loop_data.drop([u'index'], axis = 1)
    
    return loop_data


def _set_stops(loop_data):
    """Find stops in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """

    # Set the text that contains stops
    loop_data[u'stop'] = 0
    loop_data.ix[loop_data.text.str.contains(u'stop_'),u'stop'] = 1
    
    return loop_data


def _set_values(loop_data):
    """Find rows corresponding to values in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # These are the indexes of all the data that are unassigned
    value_indexes = loop_data.ix[(loop_data.loop==0)&(loop_data.tag==0)&(loop_data.stop==0)].index
    loop_data[u'value'] = 0
    loop_data.ix[value_indexes,u'value'] = 1
    
    # These are the indexes of data who follow either a loop, label, or stop tag
    value_indexes_begin = loop_data.ix[(value_indexes-1)].ix[loop_data.value==0].index + 1
    
    # The first rows of each data correspond to data for their respective loops
    loop_max = loop_data.loop.max()
    loop_range = np.arange(loop_max-1, -1, -1)
    
    for idx in value_indexes_begin:
        loop_data.ix[idx:idx+len(loop_range)-1,u'value'] += loop_range
    
    return loop_data


def _extract_loop_data(loop_data):
    """Extract the values based on pre-determined start/stop positions
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    # TODO: handle different max levels for each loop set ?
    
    # Get the outer level of the loops
    max_level = loop_data.loop.max()

    # Arrays of the start and stop indices for the outermost loops
    loop_index_begin = loop_data.ix[loop_data.loop==max_level].index
    loop_index_end = np.append(loop_index_begin[1:]-1, [len(loop_data)])

    # Loop through all the outermost loops splitting data and converting into tables for all lower levels
    outer_df_list = list()
    for lim in list(zip(loop_index_begin, loop_index_end)):

        # The data for this slice
        level_data = loop_data.ix[lim[0]:lim[1]]
        # The indices for the innermost level of data
        level_data_index = level_data.ix[level_data.value==1].index

        # Pull out the tags and values for each level and put into a table
        inner_df_list = list()
        inner_df_columns = list()
        for level in range(max_level, 0, -1):

            # The tag list and the values
            tag_list = level_data.ix[level_data.tag==level,u'text'].apply(lambda x: re.split(r"""\s+""",x))
            value_list = level_data.ix[level_data.value==level,u'text'].apply(lambda x: re.split(r"""\s+""",x))

            # Stuff the tags and values into a table
            inner_df = pd.DataFrame(value_list.tolist(), columns=tag_list.tolist()[0], index=value_list.index)
            inner_df_list.append(inner_df)
            inner_df_columns += tag_list.tolist()[0]

        # Combine all the lower levels into a single table and fill in missing data from outer levels
        outer_df = pd.concat(inner_df_list).sort_index().fillna(method=u'ffill')

        # Select just the innermost level data since the outer level data has been filled in
        outer_df = outer_df.ix[level_data_index]

        # Reorder the data columns
        outer_df = DataFrame(outer_df, columns=inner_df_columns).reset_index(drop=True)

        # Combine into a list
        outer_df_list.append(outer_df)
        
    if len(outer_df_list) == 1:
        return outer_df_list[0]
    else:
        return outer_df_list


def _convert_loops_to_df(text_loops):
    """Classify all data and convert to dataframe
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # Convert the list to a table
    df_loop = DataFrame(text_loops, columns=[u'text'])
    
    # Append columns which classify each row as a loop tag,
    # stop tag, label tab, or data values
    df_loop = _set_loops(df_loop)
    df_loop = _set_labels(df_loop)
    df_loop = _set_stops(df_loop)
    df_loop = _set_values(df_loop)
    
    # Extract the data into a table
    df_list = _extract_loop_data(df_loop)
    
    return df_list


def _clean_up_loop_dict(loop_dict):
    """Clean up loop labels in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # Remove the 'data_header' tag if it exists
    # since it is a list of dataframes
    # Then re-attach each of them one at a time
    if u'data_header' in loop_dict.keys():
        header_df_list = loop_dict.pop(u'data_header')
        
        if isinstance(header_df_list, list):
            for df in enumerate(header_df_list):
                loop_dict[u'data_header_'+str(df[0]+1)] = df[1]
        else:
            loop_dict[u'data_header_1'] = header_df_list
            
    return loop_dict


def _clean_up_table_column_names(loop_dict):
    """Clean up column names in data
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """
    
    # Make the column names all lowercase
    # and remove any underscores from the beginning
    for key in loop_dict.keys():
        rename_dict = { x:re.sub(r"""^_""", '', x.lower()) for x in loop_dict[key].columns }
        loop_dict[key].rename(columns=rename_dict, inplace=True)
        
    return loop_dict


### Functions that operate on either tag or loop data


def _coerce_and_store_data_types(tag_loop_dict):
    """Convert columns to float and integers whenever possible
       This is a private function, not meant for general use.

       Input: dataframe

       Output: dataframe
    """

    regex_format = re.compile(r"""\d*\.(?P<decimal>\d+)(?:[Ee]?[+-]?(?P<exponent>\d?))""")

    # Attempt to convert data columns from strings to integers or floats whenever possible
    # Skip any table with 'data_header' in its name because these contain mixed data
    for key in tag_loop_dict.keys():
        if u'data_header' not in key:
            tmp = tag_loop_dict[key].copy()
            tag_loop_dict[key] = tag_loop_dict[key].apply(lambda x: pd.to_numeric(x, errors=u'ignore'))
            
            # Preserve the formatting for all columns that were converted to floats
            float_cols = [x for x in tag_loop_dict[key].columns if tag_loop_dict[key][x].dtype == np.float]

            decimal_format = dict([(col, tmp[col].apply(lambda x: 
                                    len(re.search(regex_format, x).group('decimal'))).max())
                               for col in float_cols])

            exponent_format = dict([(col, tmp[col].apply(lambda x: 
                                    len(re.search(regex_format, x).group('exponent'))).max())
                               for col in float_cols])

            number_format = dict([(col,'f') if exponent_format[col] == 0 else (col,'E')
                                  for col in float_cols])

            formatter = dict([(col, '{:.' + str(decimal_format[col]) + number_format[col] + '}') 
                               for col in float_cols])
            
            # Save format instructions to dataframe
            tag_loop_dict[key]._print_format = formatter

    return tag_loop_dict

