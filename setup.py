#!/usr/bin/env python

from setuptools import setup

setup(
    name='GLHE',
    version='0',
    author="Matt Mitchell",
    author_email="mitchute@gmail.com",
    packages=['glhe'],
    long_description=open('README.md').read(),
    test_suite='nose.collector',
    tests_require=['nose'],
)
