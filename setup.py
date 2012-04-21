#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def publish():
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

dependencies = ['GitPython==0.3.2.RC1',
                'argparse==1.2.1',
                'async==0.6.1',
                'certifi==0.0.8',
                'chardet==1.0.1',
                'clint==0.3.1',
                'gitdb==0.5.4',
                'github2==0.6.0',
                'httplib2==0.7.2',
                'pbs==0.98',
                'py==1.4.6',
                'python-dateutil==1.5',
                'requests==0.10.1',
                'simplejson==2.3.2',
                'smmap==0.8.2',
                'tox==1.3',
                'virtualenv==1.7',
                'wsgiref==0.1.2',
]

setup(
    name='octogit',
    version='0.1.3',
    description='giving git tentacles to work better with github',
    url='https://github.com/myusuf3/octogit',
    author='Mahdi Yusuf',
    author_email='yusuf.mahdi@gmail.com',
    install_requires=dependencies,
    packages=['octogit', ],
    license='MIT License',
    long_description="""
========
Octogit
========

Do you hate this screen? Do you hate switching screens to see issues? Do you love the terminal? Then you will love this project.

During the development of this plugin Github smartened up and introduced a new way to create repositories. Hopefully people who like to stay in the terminal will enjoy this litle cli app.

.. image:: https://github.com/myusuf3/octogit/raw/gh-pages/assets/img/readme_image.png


Installation
============

`pip install octogit`


How to Octogit
==============

Go to http://myusuf3.github.com/octogit


Contribute
==========
If you would like to contribute simply fork this project and add yourself to the AUTHORS.txt along with some changes hopefully and submit a pull request.



    """,
    entry_points={
        'console_scripts': [
            'octogit = octogit.cli:begin',
        ],
    },
    )
