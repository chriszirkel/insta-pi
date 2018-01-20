from setuptools import setup

setup(
   name='instapi',
   version='1.0',
   description='Instragram parser and viewer for Raspberry Pi',
   author='Chris Zirkel',
   author_email='chris@zirkel.me',
   packages=['instapi'],
   install_requires=['selenium',],
)