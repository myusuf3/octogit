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
    version='0.1.1',
    description='giving git tentacles to work better with github',
    url='https://github.com/myusuf3/octogit',
    author='Mahdi Yusuf',
    author_email='yusuf.mahdi@gmail.com',
    install_requires=dependencies,
    packages=['octogit', ],
    license='MIT License',
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'octogit = octogit.cli:begin',
        ],
    },
    )
