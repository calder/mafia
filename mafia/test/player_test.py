from mafia.player import *
from mafia.util import *

from unittest import TestCase

class PlayerTest(TestCase):
  def test_player_info(self):
    info = PlayerInfo(name="Foo", bar="Bar")
    assert_equal(info.name, "Foo")
    assert_equal(info.bar, "Bar")
    with self.assertRaises(AttributeError):
      info.fizzle
