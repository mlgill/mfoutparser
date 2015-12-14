# mfoutparser
by Arthur G. Palmer, III and Michelle L. Gill

A series of python subroutines to read and extract information from the STAR format mfout file generated by the program ModelFree.

Unlike the BMRB STAR format, the format used by ModelFree uses the data_name field, rather than the save_name field and also allows nested loops. (The mfout file has loops nested to a depth of two only).

## Interactive Demo

The `mfoutparser/examples` directory contains a demonstration Jupyter notebook and sample input and output files. The notebook can be viewed (non-interactively) on GitHub [here](https://github.com/mlgill/mfoutparser/blob/master/mfoutparser/examples/MFparser_demo.ipynb). 

The interactive demo can also be run live in the web browser by clicking here: [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/mlgill/mfoutparser). After the page loads in Jupyter, click on the following to get to and load the notebook: `mfoutparser` --> `examples` --> `MFparser_demo.ipynb`.


Once `mfoutparser` has been installed, the `examples` directory can be copied to the current path using the following shell command:

```
python -c 'import mfoutparser as mf; mf.copy_examples()'
```

## Compatibility

`mfoutparser` has been tested on python 2.7, 3.4, and 3.5. It requires the `numpy` (tested on version 1.10.1) and `pandas` (version >= 0.17.1) libraries. IPython/Jupyter notebook (version >= 3.2.1) is required to run the demonstration notebook located in the `examples` directory. Matplotlib is required if plotting of the data is desired.

## Installation

`mfoutparser` can be installed with the [conda](https://anaconda.org/mlgill/mfoutparser) and [pip](https://pypi.python.org/pypi/mfoutparser) package managers or using python's `setuptools`. See the [installation instructions](https://github.com/mlgill/mfoutparser/blob/master/INSTALL.md) for more information.
