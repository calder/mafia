from mafia import *
from .test_game import TestGame

from nose_parameterized import parameterized
from unittest import TestCase

class NaturalActionResolutionTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.busdriver   = self.game.add_player("Busdriver", Busdriver(self.town))
    self.villager    = self.game.add_player("Villager", Villager(self.town))
    self.goon        = self.game.add_player("Goon", Goon(self.mafia))
    self.roleblocker = self.game.add_player("Roleblocker", Roleblocker(self.town))

  def test_roleblock_can_be_busdriven(self):
    """Test that a roleblock and be busdriven."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.busdriver)))
    night0.add_action(Busdrive(self.busdriver, self.villager, self.goon))
    night0.add_action(Roleblock(self.roleblocker, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      events.Visited(self.busdriver, self.villager),
      events.Visited(self.busdriver, self.goon),
      events.Busdriven(self.villager, self.goon),
      events.Visited(self.roleblocker, self.goon, original_target=self.villager),
      events.Blocked(self.goon),
    ], phase=night0))
    assert self.villager.alive is True

  def test_busdrive_can_be_roleblocked(self):
    """Test that a busdriver can be roleblocked."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Busdrive(self.busdriver, self.villager, self.goon))
    night0.add_action(Roleblock(self.roleblocker, self.busdriver))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      events.Visited(self.roleblocker, self.busdriver),
      events.Blocked(self.busdriver),
      events.Visited(self.goon, self.villager),
      events.Died(self.villager),
    ], phase=night0))
    assert self.villager.alive is False

  def test_real_targets_used(self):
    """
    Test that real targets, not raw targets, are used to calculate dependencies.

    This test works by setting up a kill that should be dependent on a busdriven
    rollblock. If dependencies are calculated incorrectly, however, the kill
    won't depend on the roleblock and will resolve first.
    """

    # Give the roleblock lower precedence so only an explicit
    # dependency will cause it to be resolved first.
    class LateRoleblock(Roleblock):
      precedence = Kill.precedence + 1
    class LateRoleblocker(Roleblocker):
      action = LateRoleblock(placeholders.Self(), placeholders.Player())
      precedence = Kill.precedence + 1
    self.roleblocker.add_effect(effects.ChangeRole(LateRoleblocker(self.town)))

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Busdrive(self.busdriver, self.roleblocker, self.goon))
    night0.add_action(LateRoleblock(self.roleblocker, self.roleblocker))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      events.Visited(self.busdriver, self.roleblocker),
      events.Visited(self.busdriver, self.goon),
      events.Busdriven(self.roleblocker, self.goon),
      events.Visited(self.roleblocker, self.goon, original_target=self.roleblocker),
      events.Blocked(self.goon),
    ], phase=night0))
    assert self.villager.alive is True
