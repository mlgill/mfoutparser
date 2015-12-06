#! /usr/bin/env python

from mfoutparser import DOCSTRING, VERSION

DESCRIPTION = 'mfoutparser: efficient and convenient parsing of ModelFree output files.'
LONG_DESCRIPTION = DOCSTRING

DISTNAME = 'mfoutparser'
MAINTAINER = 'Michelle Gill'
MAINTAINER_EMAIL = 'michelle@michellelynngill.com'
URL = 'https://github.com/mlgill/mfoutparser'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/mlgill/mfoutparser'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup


def check_dependencies():
    install_requires = []

    try:
        import numpy

    except ImportError:
        install_requires.append('numpy')


    try:
        import pandas

    except ImportError:
        install_requires.append('pandas')


    return install_requires


if __name__ == "__main__":

    install_requires = check_dependencies()

    setup(name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=install_requires,
        packages=['mfoutparser'],
        include_package_data = True,
        classifiers=[
                     'Intended Audience :: Science/Research',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License',
                     'Topic :: Scientific/Engineering :: Chemistry',
                     'Topic :: Scientific/Engineering :: Visualization',
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Operating System :: MacOS'],
          )

