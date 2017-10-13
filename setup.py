
'''
setup.py - Python distutils setup file for BreezySLAM package.

Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

# Support streaming SIMD extensions

from platform import machine

OPT_FLAGS  = []
SIMD_FLAGS = []

arch = machine()

if  arch == 'i686':
    SIMD_FLAGS = ['-msse3']

elif arch == 'armv7l':
    OPT_FLAGS = ['-O3']
    SIMD_FLAGS = ['-mfpu=neon']

else:
    arch = 'sisd'



SOURCES = [
    'sdk/src/rplidar_driver.cpp',
    'sdk/src/arch/linux/timer.cpp']


from distutils.core import setup, Extension

module = Extension('app/ultra_simple', 
    sources = SOURCES, 
    extra_compile_args = SIMD_FLAGS + OPT_FLAGS
    )


setup (name = 'rplidara2',
    version = '0.0',
    description = 'Module to read data from Rlidar A2',
    packages = ['app'],
    ext_modules = [module],
    author='Osmar Alcala',
    author_email='osmar.alcala@udem.edu',
    url='',
    license='',
    platforms='Linux; Windows; OS X',
    long_description = 'Provides core classes for RPLIDAR'
    )
