# -*- coding: utf-8 -*-
'''setup.py
DO NOT EDIT, update the __about__.py in your src directory with pertinent info instead.

'''

import os
from setuptools import setup, find_packages
from setuptools.command.test import test
import sys

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src", "triconf")
about = {}
with open(os.path.join(SRC_DIR, "__about__.py")) as f:
    exec(f.read(), about)

class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = [os.path.join(BASE_DIR, "tests")]
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    author=about['__author__'],
    author_email=about['__author_email__'],
    cmdclass = {'test': PyTest},
    classifiers=about['__classifiers__'], # For more classifiers, see http://goo.gl/zZQaZ
    description=about['__package_name__'].replace('_',' ').title(),
    install_requires=about['__requires__'],
    license=about['__license__'],
    long_description=about['__desc__'],
    name=about['__package_name__'],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=['tests', 'tests.*']),
    platforms='any',
    scripts=about['__scripts__'],
    tests_require=['pytest'],
    url=about['__url__'],
    version=about['__version__'],
    zip_safe=False
)

