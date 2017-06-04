# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='SaltBot',
    version='1.0.0',
    description='Bot discord',
    long_description=readme,
    author='Dubois and Ferreira',
    url='https://github.com/zKheyl/SaltBot',
    packages=find_packages()
)