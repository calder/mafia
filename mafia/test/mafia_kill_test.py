from mafia import *
from .test_game import TestGame

from nose_parameterized import parameterized
from unittest import TestCase

class MafiaKillTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager1 = self.game.add_player(Player("Villager 1", role=Villager(faction=self.town)))
    self.villager2 = self.game.add_player(Player("Villager 2", role=Villager(faction=self.town)))
    self.goon1     = self.game.add_player(Player("Goon 1", role=Goon(faction=self.mafia)))
    self.goon2     = self.game.add_player(Player("Goon 2", role=Goon(faction=self.mafia)))

  def test_mafia_kill(self):
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon1, self.villager1)))
    self.game.resolve(night0)

    assert self.villager1.alive is False
    assert_equal(self.game.log, Log([
      Visited(self.goon1, self.villager1),
      Died(self.villager1),
    ], phase=night0))

  def test_reject_multiple_mafia_kills(self):
    """Only the last kill should go through."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon1, self.villager1)))
    night0.add_action(FactionAction(self.mafia, Kill(self.goon2, self.villager2)))
    self.game.resolve(night0)

    assert self.villager1.alive is True
    assert self.villager2.alive is False
    assert_equal(self.game.log, Log([
      Visited(self.goon2, self.villager2),
      Died(self.villager2),
    ], phase=night0))
