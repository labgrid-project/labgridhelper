#!/usr/bin/env python3

from setuptools import setup

setup(
    name='labgridhelper',
    description='labgridhelper: helper functions for the labgrid library',
    author='Rouven Czerwinski',
    author_email='entwicklung@pengutronix.de',
    license='LGPL-2.1',
    use_scm_version=True,
    url='https://github.com/labgrid-project',
    python_requires='>=3.5, <3.7',
    install_requires=[
        'labgrid>=0.1.0',
    ],
    packages=[
        'labgridhelper',
    ],
    # custom PyPI classifiers
    classifiers=[
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
