#!/usr/bin/env python

import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'mackerel', '__version__.py'), 'r',
          encoding='utf-8') as f:
    exec(f.read(), about)
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r', encoding='utf-8') as f:
    changelog = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + changelog,
    url=about['__url__'],
    packages=['mackerel'],
    package_data={'': ['LICENSE'], 'mackerel': ['config.ini']},
    include_package_data=True,
    license=about['__license__'],
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'Jinja2',
        'MarkupSafe',
        'mistune',
        'mistune-contrib',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    entry_points='''
        [console_scripts]
        mackerel=mackerel.cli:cli
    ''',
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',  # noqa
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
)
