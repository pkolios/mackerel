import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('mackerel/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='mackerel',
    version=version,
    author='Paris Kolios',
    author_email='hi@enc.io',
    description='A minimalistic and unrefined static site generator '
                'built in Python 3 with typing',
    # long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Jinja2',
        'mistune',
        'mistune-contrib',
    ],
    entry_points='''
        [console_scripts]
        mackerel=mackerel.cli:cli
    ''',
)
