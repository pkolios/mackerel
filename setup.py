import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('mackerel/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='mackerel',
    version=version,
    author='Paris Kolios',
    author_email='hi@enc.io',
    url='https://github.com/pkolios/mackerel',
    download_url='https://github.com/pkolios/mackerel/archive/0.1.tar.gz',
    description='Mackerel is a minimal static site generator written in '
                'typed Python 3.6+',
    long_description=read('README.rst'),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'Jinja2',
        'MarkupSafe',
        'mistune',
        'mistune-contrib',
    ],
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
