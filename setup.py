# -*- coding: utf-8 -*-
from distutils.core import setup

with open("VERSION", "r") as fobj:
    VERSION = fobj.read()

setup(
    name='Automatictime',
    version=VERSION,
    author='Stefan Eiermann',
    author_email='foss@ultraapp.de',
    scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    url='http://gitlab.com/eieste/AutomaticTime/',
    license='LICENSE',
    description='Useful towel-related stuff.',
    long_description=open('README.md').read(),
)
