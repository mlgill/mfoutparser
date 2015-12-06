# Installation of mfoutparser

## Using Anaconda *(RECOMMENDED)*

The easiest way to install mfoutparser, its requirements (numpy and pandas), and optional requirements (Jupyter notebook and matplotlib) is to use [Andaconda](https://www.continuum.io/downloads).

After creating an environment, install numpy, pandas, Jupyter, and matplotlib according to standard installation instructions.

The, mfoutparser can be installed from a [custom built package](https://anaconda.org/mlgill/mfoutparser) for Linux or Mac OS X using the following command:

```
conda install -c mlgill mfoutparser
```

Using Anaconda automatically handles package dependencies and ensures the operating system's python installation is not over written. It also ensures mfoutparser can easily be updated and/or uninstalled later. It also ensures 

## Using pip

Alternatively, mfoutparser can be installed using the `pip` package manager like this:

```
pip install mfoutparser
```

## Using setuptools

Finally, mfoutparser can be installed using python's `setuptools`. Ensure that you understand how setuptools installations work so mfoutparser (and dependencies) are not installed in your operating system's python directory.

First, clone the github repo using the following command:

```
git clone https://github.com/mlgill/mfoutparser mfoutparser
```

Then `cd` into the downloaded directory and install mfoutparser using the following command:

```
cd mfoutparser && python setup.py install
```
