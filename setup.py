import os
import platform
import sys
from pyimg4 import version as img4
from setuptools import setup, find_packages
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = img4.VERSION

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyimg4',
    version='0.1.1',
    description='A Python library for manipulating IMG4, IM4M, and IM4P files.',
    author='Mathieu Renard',
    author_email='mathieu.renard@gotohack.org',
    url='https://github.com/gotohack/pyimg4',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'scapy',  
    ],
)

