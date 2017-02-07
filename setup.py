#!/usr/bin/env python3
from setuptools import setup
from imghost import __version__

with open("./requirements.txt") as reqf:
    deps = reqf.read().strip().split("\n")

setup(name='imghost',
      version=__version__,
      description='minimal img hoster',
      url='http://',
      author='dpedu',
      author_email='git@davepedu.com',
      packages=[
          'imghost'
      ],
      entry_points={
          'console_scripts': [
              'imghost = imghost.api:main'
          ]
      },
      install_requires=deps,
      zip_safe=False)
