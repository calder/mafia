from .test_game import *
from mafia import *

from unittest import TestCase

class ActionMatchingTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.cop  = self.game.add_player("Cop", Cop(self.town))
    self.goon = self.game.add_player("Goon", Goon(self.mafia))

  def test_simple_match(self):
    action = Investigate(self.cop, self.goon)
    assert self.cop.role.action.matches(action, game=self.game, player=self.cop)

  def test_faction_action(self):
    action = FactionAction(self.mafia, Kill(self.goon, self.cop))
    assert FactionAction(self.mafia, self.mafia.action).matches(action, game=self.game, player=self.goon)
