#! /usr/bin/python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("tttree", ["tttree.pyx"])]

setup(
  name = '2-3 Tree',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

