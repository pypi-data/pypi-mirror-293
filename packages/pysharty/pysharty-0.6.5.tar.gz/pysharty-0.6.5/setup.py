#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""soyjak.party Python Library.

pysharty is an absolutely spine chilling genre defining bone tingling
terrifying jumpscare 'jak driven atmosphere oozing a24 released
trope subverting dark and eerie gut wrenching aesthetically heavy
craft gradual escalation soul shaking dread inducing post horror
suspenseful build up a "say more with less" approach blood curdling
kino keyed nerve wracking nail biting jaw clenching free of cheap gore
kuz, soot, doll and froot approved snopes verified reuters verified
'zellig free coal killing cobson loving fauci approved pro science
truth uncovering jannie decimating glowie zapping vtuber chudding
schizophrenic 4cuck killing shitter crashing discoal erasing
'coinslot closing NAS free anti meds soylent free wholesome pupperino
west rising heavenly holy sharty saving IAS gemerald Python library that gives access to the soyjak.party API
and an object-oriented way to browse and get board and thread
information quickly and easily.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
the LICENSE file for more details.
"""

from setuptools import setup

setup(
    name='pysharty',
    version='0.6.5',
    description=("Python soyjak.party API Wrapper. Based on BASC-py4chan by the Bibliotheca Anonoma"),
    license=open('LICENSE').read(),
    author='Antonizoon Overtwater',
    author_email='antonizoon@bibanon.org',
    url='http://github.com/SuperWaluigi64/pysharty',
    packages=['pysharty'],
    package_dir={
        'pysharty': 'pysharty',
    },
    package_data={'': ['README.rst', 'LICENSE']},
    install_requires=['requests >= 1.0.0'],
    keywords='soyjak.party api',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
