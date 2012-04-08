#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


dependencies = ['clint>=0.2.1', 'requests']

setup(
    name='octogit',
    version='0.1dev',
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
