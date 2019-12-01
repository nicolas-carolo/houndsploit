#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages
import os
import sys


setup(name='houndsploit',
      version='2.0.0',
      description='An advanced graphic search engine for Exploit-DB',
      keywords='houndsploit',
      author='Nicolas Carolo',
      author_email='nicolascarolo.dev@gmail',
      url='https://github.com/nicolas-carolo/houndsploit',
      license='3-clause BSD',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   ],
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=[],
      entry_points={
           'console_scripts':[
               'houndsploit = HoundSploit.main:main',
           ]
      },
      )

base_path = os.path.dirname(os.path.realpath(__file__))
init_path = os.path.split(sys.executable)[0]
if not os.path.isdir(init_path + '/HoundSploit'):
    os.system('mkdir ' + init_path + '/HoundSploit')
os.system('cp -r ' + base_path + '/HoundSploit/templates ' + init_path + '/HoundSploit')
os.system('cp -r ' + base_path + '/HoundSploit/static ' + init_path + '/HoundSploit')
if not os.path.isdir(init_path + '/HoundSploit/csv'):
    os.system('mkdir ' + init_path + '/HoundSploit/csv')
os.system('cp -r ' + base_path + '/HoundSploit/searcher/suggestions.csv ' + init_path + '/HoundSploit/csv')