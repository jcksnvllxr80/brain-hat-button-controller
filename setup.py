from ez_setup import use_setuptools

use_setuptools()
from setuptools import setup, find_packages

setup(name='remote_buttons',
      version='1.1.0',
      author='Aaron Watkins',
      author_email='ac.watkins80@gmail.com',
      description='Control a pi camera remotely with REST.',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pyyaml',
          'flask_cors',
      ])