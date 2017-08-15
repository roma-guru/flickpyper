#!/usr/bin/env python

from distutils.core import setup
from flickpyper.main import VERSION

setup(name='flickpyper',
      version=VERSION,
      description='Fresh wallpapers from Flickr',
      long_description=open('README.md').read(),
      author='Roman Voropaev',
      author_email='voropaev.roma@gmail.com',
      url='https://github.com/roman-voropaev/flickpyper',
      keywords='flickr wallpaper',
      packages=['flickpyper'],
      classifiers=[]
)
