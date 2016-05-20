from setuptools import *

setup(
  # Metadata
  name="mafia",
  version="0.6",
  author="Calder Coalson",
  author_email="caldercoalson@gmail.com",
  url="https://github.com/calder/mafia",
  description="A library for moderating games of Mafia.",
  long_description="See https://github.com/calder/mafia for documentation.",

  # Contents
  packages=find_packages(exclude=["*.test"]),

  # Dependencies
  install_requires=[
    "termcolor",
  ],
  setup_requires=[
    "nose",
  ],
  tests_require=[
    "nose-parameterized",
  ],

  # Settings
  test_suite="nose.collector",
  zip_safe=True,
)
