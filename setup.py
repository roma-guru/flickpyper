#!/usr/bin/env python

from distutils.core import setup
from flickpyper.config import VERSION
from sys import platform
#from cx_Freeze import setup, Executable

setup(name='flickpyper',
      version=VERSION,
      description='Fresh wallpapers from Flickr and Unsplash',
      long_description=open('README.md').read(),
      author='Roman Voropaev',
      author_email='voropaev.roma@gmail.com',
      license='MIT',
      url='https://github.com/roman-voropaev/flickpyper',
      keywords='flickr wallpaper desktop',
      packages=['flickpyper'],
      scripts=['bin/flickpyper'],
      install_requires=['flickrapi','wget'] +
                ['appscript'] if platform=='darwin' else [],
      data_files=[('',['README.md'])],
      #executables=[Executable('bin/flickpyper')],
      python_requires='>=3.6',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ]
)
