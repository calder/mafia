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
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.busdriver)))
    night0.add_action(Busdrive(self.busdriver, self.villager, self.goon))
    night0.add_action(Roleblock(self.roleblocker, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      Visited(self.busdriver, self.villager),
      Visited(self.busdriver, self.goon),
      Visited(self.roleblocker, self.goon, original_target=self.villager),
      WasBlocked(self.goon),
    ], phase=night0))
    assert self.villager.alive is True

  def test_busdrive_can_be_roleblocked(self):
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Busdrive(self.busdriver, self.villager, self.goon))
    night0.add_action(Roleblock(self.roleblocker, self.busdriver))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      Visited(self.roleblocker, self.busdriver),
      WasBlocked(self.busdriver),
      Visited(self.goon, self.villager),
      Died(self.villager),
    ], phase=night0))
    assert self.villager.alive is False
