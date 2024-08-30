# setup.py
from setuptools import setup, find_packages

setup(
    name='picodingchallenge_rb',  # Your package name
    version='0.1.0',  # Initial release version
    author='Ridwan Basith',
    author_email='ridwanbasith93@gmail.com',
    description='a Python package designed to complete a coding challenge I was set.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find the packages
    install_requires=[  # List of dependencies
        'pandas',
        'beautifulsoup4',
        'requests',
        'regex',
        'os',
        'io',
        'datetime',
        'csv',
        'json',
        'logging'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
