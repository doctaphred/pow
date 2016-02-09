#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='pow',
    version='0.0.1',
    description=(
        "Command line text snippets, inspired by Zach Holman's **boom**."),
    url='https://github.com/doctaphred/pow',
    author='Frederick Wagner',
    author_email='doctaphred@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
    keywords=['command line', 'text', 'snippet', 'snippets', 'clipboard'],
    py_modules=['pow'],
    install_requires=requirements,
    extras_require={
        'test': ['flake8'],
        },
    entry_points={
        'console_scripts': [
            'pow = pow:main',
            ],
        },
    )
