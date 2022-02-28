# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2022 RERO.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds administration panel to the system."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'invenio-theme>=1.3.4',
    'pytest-invenio>=1.4.3',
]

extras_require = {
    'docs': [
        'Sphinx>=4.2.0',
    ],
    'access': [
        'invenio-access>=1.0.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask-Admin>=1.5.6',
    'Flask-Menu>=0.5.0',
    'Flask-Principal>=0.4.0',
    'invenio-accounts>=1.2.1',
    'invenio-base>=1.2.9',
    'invenio-db>=1.0.9',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_admin', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-admin',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio admin flask-admin',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-admin',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_admin = invenio_admin:InvenioAdmin',
        ],
        'invenio_base.blueprints': [
            'invenio_admin = invenio_admin.views:blueprint',
        ],
        'invenio_access.actions': [
            'admin_access = invenio_admin.permissions:action_admin_access',
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
