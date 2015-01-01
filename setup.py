#!/usr/bin/env python

import AvivoreXT
from setuptools import setup, find_packages

dependencies = ['twitter']

scripts = ['avivore']

setup(name='AvivoreXT',
      version=AvivoreXT.__version__,
      description='Twitter data mining tool',
      long_description=open("./README.md", "r").read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
      ],
      author='@_rc0r',
      url='https://github.com/rc0r/AvivoreXT',
      install_requires = dependencies,
      scripts=scripts,
      packages=find_packages(),
)
