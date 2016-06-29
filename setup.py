'''
Created on Jun 28, 2015

@author: Gaurav Ghimire <gaurav.ghimire@gmail.com>
'''
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pycloudfs',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='commercial',  # example license
    description='Helper classes/scripts to access s3 and gridfs',
    long_description=README,
    url='https://github.com/gaumire/pycloudfs',
    author='Gaurav Ghimire',
    author_email='gaurav.ghimire@gmail.com',
    maintainer='Patrick Senti',
    classifiers=[
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: Commercial',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'mongoengine>=0.10.6',
        'boto>=2.38.0',
        'boto3>=1.1.1',
        'botocore>=1.1.12'
    ],
    dependency_links=[
    ]
)
