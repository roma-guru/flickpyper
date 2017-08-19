#!/usr/bin/env python

from distutils.core import setup
from flickpyper.config import VERSION
from sys import platform

setup(name='flickpyper',
      version=VERSION,
      description='Fresh wallpapers from Flickr',
      long_description=open('README.md').read(),
      author='Roman Voropaev',
      author_email='voropaev.roma@gmail.com',
      url='https://github.com/roman-voropaev/flickpyper',
      keywords='flickr wallpaper',
      packages=['flickpyper'],
      scripts=['bin/flickpyper.bat' if platform()=='win32' else 'bin/flickpyper'],
      install_requires=['flickrapi','wget'],
      classifiers=[]
)
