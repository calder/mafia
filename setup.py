from setuptools import *

setup(
  # Metadata
  name="mafia",
  version="0.1",
  author="Calder Coalson",
  author_email="caldercoalson@gmail.com",
  url="https://github.com/calder/mafia",
  description="Mafia library.",
  long_description="See https://github.com/calder/mafia/ for documentation.",

  # Contents
  packages=find_packages(),

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
