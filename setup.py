#!/usr/bin/env python

import AvivoreXT
from setuptools import setup, find_packages

dependencies = ['twitter']
used_license = 'GNU Library or Lesser General Public License (LGPL)'
scripts = ['avivore']

setup(name='AvivoreXT',
      version=AvivoreXT.__version__,
      description='Twitter data mining tool',
      long_description=open("./README.md", "r").read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: ' + used_license,
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      platforms=[
          'Any',
      ],
      license=used_license,
      author='rc0r',
      author_email='hlt99@blinkenshell.org',
      url='https://github.com/rc0r/AvivoreXT',
      install_requires = dependencies,
      scripts=scripts,
      packages=find_packages(),
      test_suite='tests',
)
