#mockredis/setup.py
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
]

tests_require = requires + [
]

setup(name='mockredis',
      version='0.1dev',
      description='A mock redis object.',
      long_description=README + '\n\n' + CHANGES,
      install_requires=requires,
      tests_require=tests_require,
      packages=['mockredis'],
      test_suite='mockredis.tests'
)
