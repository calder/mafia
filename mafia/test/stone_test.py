from mafia import *
from .test_game import TestGame

from unittest import TestCase, skip

class StoneTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.villager   = self.game.add_player("Villager", Villager(self.town))
    self.vigilante1 = self.game.add_player("Vigilante 1", Vigilante(self.town))
    self.vigilante2 = self.game.add_player("Vigilante 2", Vigilante(self.town))

    # TODO: Replace with a true Stone role.
    self.villager.add_effect(Stoned())

  @skip("Not implemented yet.")
  def test_basic_stone(self):
    """Stone should only apply the first night the player is killed."""

    night1 = Night(1)
    night1.add_action(Kill(self.vigilante1, self.villager))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.vigilante1, self.villager),
      events.Protected(self.villager),
    ], phase=night1))
    assert self.villager.alive

    night2 = Night(2)
    night2.add_action(Kill(self.vigilante1, self.villager))
    self.game.resolve(night2)

    assert_equal(self.game.log.phase(night2), Log([
    ], phase=night2))
    assert not self.villager.alive

  @skip("Not implemented yet.")
  def test_stone_double_kill(self):
    """Stone should only apply the first time a player is killed in a given night."""

    night1 = Night(1)
    night1.add_action(Kill(self.vigilante1, self.villager))
    night1.add_action(Kill(self.vigilante2, self.villager))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.vigilante1, self.villager),
      events.Protected(self.villager),
      events.Visited(self.vigilante2, self.villager),
      events.Died(self.villager),
    ], phase=night1))
    assert not self.villager.alive
