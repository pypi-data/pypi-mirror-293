#!/usr/bin/env python

import platform
import sys

from setuptools import setup

is_win = sys.platform.startswith('win')
is_cpython = platform.python_implementation() == 'CPython'

if len(sys.argv) <= 1:
    print("""
Suggested setup.py parameters:

    * build
    * install
    * develop (instead of install)
    * sdist  --formats=zip
    * sdist  # NOTE requires tar/gzip commands

    python -m pip install -e .

PyPi:

    python -m pip install setuptools twine

    python setup.py sdist
    # python setup.py sdist --formats=zip
    python -m twine upload dist/* --verbose

    ./setup.py  sdist ; twine upload dist/* --verbose

""")

install_requires = ["six >= 1.7.3", ]
if is_win and is_cpython:
      install_requires += ['windows-curses']

exec(open("percol/info.py").read())

person_name = 'clach04'
person_email = None

setup(name             = "percolator",
      version          = __version__,
      author           = "mooz",
      author_email     = "stillpedant@gmail.com",
      maintainer = person_name,
      maintainer_email = person_email,

      url              = "https://github.com/clach04/percolator/tree/mymain",
      description      = "Adds flavor of interactive filtering to the traditional pipe concept of shell",
      long_description = __doc__,
      packages         = ["percol"],
      scripts          = ["bin/percol"],
      classifiers      = ["Environment :: Console :: Curses",
                          "License :: OSI Approved :: MIT License",
                          "Operating System :: POSIX",
                          'Operating System :: OS Independent',
                          "Programming Language :: Python",
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.6',  # Python 3.6.9
                          'Programming Language :: Python :: 3.12',
                          "Topic :: Text Processing :: Filters",
                          "Topic :: Text Editors :: Emacs",
                          "Topic :: Utilities"],
      keywords         = "anything.el unite.vim dmenu shell pipe filter curses",
      license          = "MIT",
      install_requires = install_requires,
      extras_require={
        "cmigemo": ["cmigemo >= 0.1.5"],
        "pinyin": ["pinyin"],  # untested
        'all': ['cmigemo >= 0.1.5', "pinyin"],  # convience, all of the above
      }
      )
