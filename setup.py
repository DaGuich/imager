#!/usr/bin/env python3

from distutils.core import setup

if __name__ == '__main__':
    setup(name='imoger',
          version='0.1.0',
          description='Tool to rename a photography library images to the dates contained in their EXIF data',
          author='Matthias Gilch',
          author_email='matthias.gilch.mg@gmail.com',
          install_requires=[
            'exif'
          ],
          py_modules=['imoger'],
          scripts=['imoger.py'])
