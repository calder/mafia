import os
import re
from termcolor import colored
from unittest import TestCase

class ReadMeTest(TestCase):
  def setUp(self):
    readme_path = os.path.join(os.path.dirname(__file__), "../../README.md")
    with open(readme_path) as file:
      self.readme = file.read()

  def test_python_blocks(self):
    block_re = re.compile(r"""```python\n(.*?)\n```""", re.MULTILINE + re.DOTALL)
    matches = re.findall(block_re, self.readme)
    for match in matches:
      print("---------ReadMeTest: exec()ing:---------")
      for i, line in enumerate(match.split("\n"), start=1):
        print("%s %s" % (colored("%2d:" % i, "yellow"), line))
      print("----------------------------------------")
      exec(compile(match, "<CODE BLOCK>", "exec"))
