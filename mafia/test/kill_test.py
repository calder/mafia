from mafia import *
from .test_game import TestGame

from unittest import TestCase, skip

class KillTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.villager   = self.game.add_player("Villager", Villager(self.town))
    self.vigilante1 = self.game.add_player("Vigilante 1", Vigilante(self.town))
    self.vigilante2 = self.game.add_player("Vigilante 2", Vigilante(self.town))

  def test_double_kill(self):
    """Only the first kill in a given night succeeds."""

    night1 = Night(1)
    night1.add_action(Kill(self.vigilante1, self.villager))
    night1.add_action(Kill(self.vigilante2, self.villager))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.vigilante1, self.villager),
      events.Died(self.villager),
      events.Visited(self.vigilante2, self.villager),
    ], phase=night1))
    assert not self.villager.alive
