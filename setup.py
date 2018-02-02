try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name='osu_map_parser',
  version='0.0.1',
  author='Kir Chou',
  author_email='note351@hotmail.com',
  packages=['osu_map_parser'],
  url='https://github.com/note35/osu_map_parser',
  license='LICENSE.txt',
  description='A library written in Python for parsing map in osu',
  download_url='https://github.com/note35/osu_map_parser/archive/master.zip',
  keywords=['python', 'osu', 'parser'],
  classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Natural Language :: English",
  ]
)
