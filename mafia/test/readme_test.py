import re
from termcolor import colored
from unittest import TestCase

class ReadMeTest(TestCase):
  def setUp(self):
    self.readme = open("README.md").read()

  def exec_block(self, regex):
    match = re.search(regex, self.readme, re.MULTILINE + re.DOTALL)
    if match:
      print("---------ReadMeTest: exec()ing:---------")
      for i, line in enumerate(match.group(1).split("\n"), start=1):
        print("%s %s" % (colored("%2d:" % i, "yellow"), line))
      print("----------------------------------------")
      exec(compile(match.group(1), "<CODE BLOCK>", "exec"))
    else:
      raise RuntimeError("Block not found.")

  def test_usage(self):
    return self.exec_block(r"""## Usage\n\n```python\n(.*?)\n```""")
