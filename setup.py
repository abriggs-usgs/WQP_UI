"""
Created on Aug 26, 2016

@author: ayan
"""
import os
import sys
from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements]
    return install_requires


def read(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return content


def run_karma_tests():
    os.system('karma start test/js/karma.conf.js --no-single-run --browsers "" --reporters progress')

if sys.argv[-1] == 'karma':
    run_karma_tests()
    sys.exit()


def static_file_collect():
    os.system('python manage.py collect')

if sys.argv[-1] == 'collect':
    static_file_collect()
    sys.exit()


setup(name='usgs_flask_wqp_ui',
      version='1.0',
      description='USGS Flask Water Quality Portal User Interface',
      author='Mary Bucknell, James Kreft, Andrew Yan',
      author_email='jkreft@usgs.gov',
      packages=find_packages(),
      include_package_data=True,
      long_description=read('README.md'),
      data_files=[('instance', [])],
      install_requires=read_requirements(),
      platforms='any',
      test_suite='tests'
      )