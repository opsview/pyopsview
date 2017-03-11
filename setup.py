#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from setuptools import setup, find_packages

PYOPSVIEW_VERSION = '5.3.1'

with open('README.md', 'r') as fno:
    LONG_DESCRIPTION = fno.read()

with open('requirements.txt', 'r') as fno:
    PYOPSVIEW_REQUIRES = fno.readlines()

package = {
    'name': 'pyopsview',
    'version': PYOPSVIEW_VERSION,
    'description': 'Python client for the Opsview API',
    'long_description': LONG_DESCRIPTION,

    'maintainer': 'Joshua Griffiths',
    'maintainer_email': 'joshua.griffiths@opsview.com',
    'url': 'https://github.com/jpgxs/pyopsview',
    'download_url': 'https://github.com/jpgxs/pyopsview',

    'packages': find_packages(),
    'package_dir': {
        'pyopsview': 'pyopsview',
    },
    'package_data': {
        'pyopsview': ['README.md', 'schemas/*.json'],
    },
    'include_package_data': True,
    'install_requires': PYOPSVIEW_REQUIRES,
}

setup(**package)
