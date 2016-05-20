from mafia import *
from .test_game import TestGame

from unittest import TestCase

class RoleModifierTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))

  def test_ninja(self):
    # Action-less Ninjas aren't allowed.
    with self.assertRaises(AssertionError):
      self.game.add_player("Crappy Ninja", Ninja(self.mafia))

    # Ninjas must have either an action or a faction_action.
    self.game.add_player("Good Ninja", Ninja(Tracker(self.town)))
    self.game.add_player("Evil Ninja", Ninja(Goon(self.mafia)))

  def test_overeager(self):
    # Action-less Overeagers aren't allowed.
    with self.assertRaises(AssertionError):
      self.game.add_player("Overeager ???", Overeager(self.mafia))
    with self.assertRaises(AssertionError):
      self.game.add_player("Overeager ???", Overeager(Goon(self.mafia)))

    # Overeagers must have either an action or a faction_action.
    self.game.add_player("Overeager Tracker", Overeager(Tracker(self.town)))
