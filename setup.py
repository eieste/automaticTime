# -*- coding: utf-8 -*-
from distutils.core import setup

with open("./VERSION", "r") as fobj:
    VERSION = fobj.read()

setup(
    name='automatictime',
    version=VERSION,
    author='Stefan Eiermann',
    author_email='foss@ultraapp.de',
    #scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    url='http://gitlab.com/eieste/AutomaticTime/',
    packages=['automatictime'],
    install_requires=['marshmallow', 'piny'],
    license='LICENSE',
    description='Collects working hours from the pc and sends it to mocoapp.',
    long_description=open('README.md').read(),
)
