from distutils.core import setup
import setuptools
packages = ['kapaau']
setup(name='kapaau',
	version='1.2',
	author='szblack',
    packages=packages, 
    package_dir={'requests': 'requests'},)