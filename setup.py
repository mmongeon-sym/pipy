# coding: utf-8

from __future__ import unicode_literals
import sys

from setuptools import setup
import os
from codecs import open  # pylint:disable=redefined-builtin


here = os.path.abspath(os.path.dirname(__file__))

# Docs: https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py

# Example: https://github.com/psf/requests/blob/master/setup.py
if sys.argv[-1] == 'build':
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()

packages = ['pipy']


CLASSIFIERS = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]

about = {}

with open(os.path.join(here, 'pipy', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
        name=about['__title__'],
        version=about['__version__'],
        description=about['__description__'],
        long_description=readme,
long_description_content_type='text/markdown',
        author=about['__author__'],
        author_email=about['__author_email__'],
        url='https://github.com/mmongeon-sym/pipy',
        project_urls={
                'Documentation': 'https://github.com/mmongeon-sym/pipy',
                'Source':        'https://github.com/mmongeon-sym/pipy',
                },
        pyhon_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*,! =3.3.*, !=3.4.*,!=3.5.*, !=3.6.*, >=3.7.*, <4',
        packages=['pipy'],
        package_dir={'pipy': 'pipy'},
        classifiers=CLASSIFIERS,
        keywords='pip package',
        license='Unlicense, no rights reserved, https://unlicense.org/',
        )


