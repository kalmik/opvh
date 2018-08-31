#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='opvh',
      version='1.0',
      description='Opensips Pseudo Variables Helper.',
      author='Sergio Filipe',
      author_email='sergio.kalmik@gmail.com',
      url='',
      packages=['opvh'],
      scripts=['bin/opvh'],
      python_requires='>=3.0.*',
      install_requires=[
        "beautifulsoup4" 
      ]
     )
