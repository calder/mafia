from .test_game import *
from mafia import *

from unittest import TestCase

class ActionValidationTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.cop  = self.game.add_player("Cop", Cop(self.town))
    self.goon = self.game.add_player("Goon", Goon(self.mafia))

  def test_simple_match(self):
    """Only the player should be able to take their own action."""
    action = Investigate(self.cop, self.goon)
    assert self.cop.role.action.matches(action, game=self.game, player=self.cop)

    action = Investigate(self.goon, self.goon)
    assert not self.cop.role.action.matches(action, game=self.game, player=self.cop)

  def test_faction_action(self):
    """Only a faction member should be able to use the faction's action."""
    action = FactionAction(self.mafia, Kill(self.goon, self.cop))
    assert FactionAction(self.mafia, self.mafia.action).matches(action, game=self.game, player=self.goon)

    action = FactionAction(self.mafia, Kill(self.cop, self.cop))
    assert not FactionAction(self.mafia, self.mafia.action).matches(action, game=self.game, player=self.goon)

  def test_compelled_action(self):
    """Compelled actions should randomly select a target when none is chosen."""
    self.cop.role.action = Compelled(self.cop.role.action)

    action = Investigate(self.cop, self.goon)
    _, selected = self.cop.role.action.select_action([action], game=self.game, player=self.cop)
    assert_matches(action, selected)

    _, selected = self.cop.role.action.select_action([], game=self.game, player=self.cop)
    assert_matches(Investigate(self.cop, Placeholder.AnyPlayer()), selected)
