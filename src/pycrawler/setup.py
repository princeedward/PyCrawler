from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='pycrawler',
      version=version,
      description="A highly modularized, easy config and scale python crawler",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python crawler nosql-cache',
      author='Yunkai Cui',
      author_email='princealva@hotmail.com',
      url='https://github.com/princeedward/PyCrawler',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'cython',       # http://cython.org
          'redis',        # https://github.com/andymccurdy/redis-py
          'lxml',         # http://lxml.de/
          'reppy',        # https://github.com/seomoz/reppy
          'httplib2',     # https://github.com/jcgregorio/httplib2
          'adns-python',  # https://code.google.com/p/adns-python/
          'protobuf==2.5',     # https://developers.google.com/protocol-buffers/docs/pythontutorial
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
