#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="ionread",
    version="1.0.10",
    author="Boris Salimov",
    packages=['ionread'],
    package_data={'ionread': ['ionreader-driver'], },
    package_dir={
        'ionread': '.',
    },
)
