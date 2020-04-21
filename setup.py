#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages
import os
import sys
import getpass


setup(name='houndsploit',
      version='2.1.0',
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

try:
    print(getpass.getuser() == 'root')
    if getpass.getuser() == 'root':
        f = open(os.path.expanduser("~") + "/HoundSploit/houndsploit_sw.lock")
        f.close()
        os.remove(os.path.expanduser("~") + "/HoundSploit/houndsploit_sw.lock")
    else:
        if os.environ['SUDO_USER']:
            f = open(os.path.expanduser('~' + os.environ["SUDO_USER"]) + "/HoundSploit/houndsploit_sw.lock")
            f.close()
            os.remove(os.path.expanduser('~' + os.environ["SUDO_USER"]) + "/HoundSploit/houndsploit_sw.lock")
        else:
            f = open(os.path.expanduser("~") + "/HoundSploit/houndsploit_sw.lock")
            f.close()
            os.remove(os.path.expanduser("~") + "/HoundSploit/houndsploit_sw.lock") 
except IOError:
    pass

