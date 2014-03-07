#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='fuckitdb',
    version='0.1.3',
    description='fuckitdb is a Python ORM for Google Drive Spreadsheets.',
    long_description=readme + '\n\n' + history,
    author='Nick Johnstone',
    author_email='ncwjohnstone@gmail.com',
    url='https://github.com/Widdershin/fuckitdb',
    packages=[
        'fuckitdb',
    ],
    package_dir={'fuckitdb': 'fuckitdb'},
    include_package_data=True,
    install_requires=[
        'gspread'
    ],
    license="MIT",
    zip_safe=False,
    keywords='fuckitdb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)