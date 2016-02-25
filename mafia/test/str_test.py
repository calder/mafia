from mafia import *

from unittest import TestCase

class StrTest(TestCase):
  def test_nested_role(self):
    mafia = Mafia("The Sopranos")
    ninja_hitman = Ninja(Hitman(mafia))
    assert_equal(str(ninja_hitman), "Mafia Ninja Hitman")
