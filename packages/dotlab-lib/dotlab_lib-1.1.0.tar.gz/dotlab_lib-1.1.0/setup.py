from setuptools import find_packages, setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dotlab-lib',
    packages=find_packages(include=['dotlab']),
    version='1.1.0',
    description='DotLAB Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='DotLAB Brazil',
    author_email="igorviort@gmail.com",
    license='MIT',
    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.0.0'],
    test_suite='tests',
    include_package_data=True
)
