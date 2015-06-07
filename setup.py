#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    dependencies = [l.strip() for l in f]

setup(
    name='CodeforcesRunner',
    version='0.2.0',
    description='A simple tool to run Codeforces testcases',
    long_description=long_description,
    url='https://github.com/sayuan/CodeforcesRunner',
    author='Shiao-An Yuan',
    author_email='sayuan@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='codeforces',
    packages=['cfrun'],
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'cfrun=cfrun.cfrun:main',
        ],
    },
)
