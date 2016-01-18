from mafia.util import *

import unittest

class TestUtil(unittest.TestCase):
  def test_identitydefaultdict(self):
    d = identitydefaultdict()
    assert d[123] == 123
    d[123] = 456
    assert d[123] == 456

  def test_has_method(self):
    assert has_method([1,2,3], "append")
    assert not has_method([1,2,3], "foozle")
