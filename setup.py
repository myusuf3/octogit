#!/usr/bin/env python

"""
========
Octogit
========

Do you hate this screen? Do you hate switching screens to see issues? Do you love the
terminal? Then you will love this project.

During the development of this plugin Github smartened up and introduced a new way to
create repositories. Hopefully people who like to stay in the terminal will enjoy this
little cli app.

.. image:: https://github.com/myusuf3/octogit/raw/gh-pages/assets/img/readme_image.png


Installation
============

`pip install octogit`


How to Octogit
==============

Go to http://myusuf3.github.com/octogit


Contribute
==========
If you would like to contribute simply fork this project and add yourself to the
AUTHORS.txt along with some changes hopefully and submit a pull request.

"""

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from octogit import __version__

def publish():
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

dependencies = ['clint2','requests']

setup(
    name='octogit',
    version=".".join(str(x) for x in __version__),
    description='giving git tentacles to work better with github',
    url='https://github.com/myusuf3/octogit',
    author='Mahdi Yusuf',
    author_email='yusuf.mahdi@gmail.com',
    install_requires=dependencies,
    tests_require=['tox==1.3'],
    packages=['octogit', ],
    license='MIT License',
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'octogit = octogit.cli:begin',
        ],
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
    )
