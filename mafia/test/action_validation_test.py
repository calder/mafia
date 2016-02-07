from .test_game import *
from mafia import *

from unittest import TestCase, main

class ActionValidationTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.cop  = self.game.add_player("Cop", Cop(self.town))
    self.goon = self.game.add_player("Goon", Goon(self.mafia))

  def test_simple_match(self):
    """Only the player should be able to take their own action."""
    assert     self.cop.action.matches(Investigate(self.cop, self.goon))
    assert not self.cop.action.matches(Investigate(self.goon, self.goon))

  def test_faction_action(self):
    """Only a faction member should be able to use the faction's action."""
    assert     self.mafia.action.matches(FactionAction(self.mafia, Kill(self.goon, self.cop)))
    assert not self.mafia.action.matches(FactionAction(self.mafia, Kill(self.cop, self.cop)))

  def test_compelled_action_matching(self):
    """Compelled actions should match their concrete counterparts."""
    assert     Compelled(self.cop.action).matches(Investigate(self.cop, self.goon))
    assert not Compelled(self.cop.action).matches(Investigate(self.goon, self.goon))

  def test_compelled_action_with_choice(self):
    """Compelled actions should respect the player's choice when possible."""
    self.cop.role.action = Compelled(self.cop.role.action)

    night0 = Night(0)
    night0.add_action(Investigate(self.cop, self.goon))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.cop, self.goon),
      events.InvestigationResult(Alignment.evil, target=self.goon, to=self.cop),
    ], phase=night0))

  def test_compelled_action_no_choice(self):
    """Compelled actions should randomly select a target when none is chosen."""
    self.cop.role.action = Compelled(self.cop.role.action)

    night0 = Night(0)
    self.game.resolve(night0)

    assert_equal(2, len(self.game.log.phase(night0)))

if __name__ == "__main__":
  main()
