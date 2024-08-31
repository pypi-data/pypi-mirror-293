from setuptools import setup, find_packages
from pkg_resources import require, DistributionNotFound
import os

try:
    filename = os.path.join(os.path.dirname(__file__), 'README.txt')
    description = file(filename).read()
except:
    description = ''


install_requires = ['pillow']

version = '0.2.0'

setup(name='cropresize',
      version=version,
      description="crop and resize an image without doing the math yourself",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image',
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://pypi.python.org/pypi/cropresize',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      crop-resize = cropresize:main
      """,
      )
