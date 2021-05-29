from ez_setup import use_setuptools

use_setuptools()
from setuptools import setup, find_packages

setup(name='CameraButtons',
      version='1.0.1',
      author='Aaron Watkins',
      author_email='ac.watkins80@gmail.com',
      description='Control a pi camera remotely with REST.',
      license='MIT',
      packages=find_packages())
