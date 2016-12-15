#!/usr/bin/env python3

from setuptools import setup
from mutti import __version__

setup(name='mutti',
      version=__version__,
      description="mutti - Michael's User Text Terminal Interface",
      author='Michael Krieger',
      author_email='michael.krieger@ziti.uni-heidelberg.de',
      packages=['mutti'],
      package_data={'mutti': ['templates/*.py',
                              'examples/*.py',
                              'curses-tests/*.py',
                             ]},
      )


