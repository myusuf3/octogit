
try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup


dependencies = ['clint>=0.2.1', 'requests']

setup(
    name='hub',
    version='0.1dev',
    description='simple interface for creating repositories and other things',
    url='https://github.com/myusuf3/hub',
    author='Mahdi Yusuf',
    author_email='yusuf.mahdi@gmail.com',
    install_requires=dependencies,
    packages=['hub',],
    license='MIT License',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'hub = hub.cli:begin',
        ],
    },
    )
