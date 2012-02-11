
try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

setup(
    name='hub',
    version='0.1dev',
    description='simple interface for creating repositories',
    url='https://github.com/myusuf3/hub',
    author='Mahdi Yusuf',
    author_email='yusuf.mahdi@gmail.com',
    packages=['hub',],
    license='MIT License',
    long_description=open('README.rst').read(),
    )
