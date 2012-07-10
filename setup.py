#mockredis/setup.py
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.md')).read()
except IOError:
    CHANGES = README = ''

requires = [
]

tests_require = requires + [
]

setup(name='mockredis',
      version='0.1.3dev',
      description='A mock redis object.',
      long_description=README + '\n\n' + CHANGES,
      install_requires=requires,
      tests_require=tests_require,
      packages=['mockredis'],
      test_suite='mockredis.tests'
)
