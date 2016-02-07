from mafia import *
from .test_game import TestGame

from unittest import TestCase

class WinnerTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.villager3 = self.game.add_player("Villager 3", Villager(self.town))
    self.goon1     = self.game.add_player("Goon 1", Goon(self.mafia))
    self.goon2     = self.game.add_player("Goon 2", Goon(self.mafia))

  def test_mafia_win(self):
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.villager3.alive = False
    assert_equal(self.game.winners(), [self.goon1, self.goon2])

  def test_town_win(self):
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.goon1.alive = False
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.goon2.alive = False
    assert_equal(self.game.winners(), [self.villager1, self.villager2, self.villager3])

  def test_usurper_win(self):
    usurper = self.game.add_player("Usurper", Usurper(self.mafia, self.goon2))
    self.villager1.alive = False
    self.goon2.alive = False
    assert_equal(self.game.winners(), [self.goon1, self.goon2, usurper])

  def test_usurper_loss(self):
    usurper = self.game.add_player("Usurper", Usurper(self.mafia, self.goon1))
    assert_equal(self.game.winners(), [self.goon1, self.goon2])

  def test_godfather_alignment(self):
    self.goon1.alive = False
    self.goon2.alive = False
    assert_equal(self.game.winners(), [self.villager1, self.villager2, self.villager3])

    godfather = self.game.add_player("Godfather", Godfather(self.mafia))
    assert_equal(self.game.winners(), NO_WINNER_YET)
