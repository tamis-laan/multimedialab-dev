from distutils.core import setup, Extension
module1 = Extension('window', sources = ['window.c'])
setup (name = 'window',version = '1.0',description = 'This implements a sliding window',ext_modules = [module1])
