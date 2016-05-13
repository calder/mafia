from mafia import *
from .test_game import TestGame

from unittest import TestCase

class WinnerTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town   = self.game.add_faction(Town())
    self.mafia  = self.game.add_faction(Mafia("Mafia"))
    self.jokers = self.game.add_faction(JokerFaction("Jokers"))
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.villager3 = self.game.add_player("Villager 3", Villager(self.town))
    self.goon1     = self.game.add_player("Goon 1", Goon(self.mafia))
    self.goon2     = self.game.add_player("Goon 2", Goon(self.mafia))
    self.joker     = self.game.add_player("Joker", Joker(self.jokers))

  def test_mafia_wins(self):
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.villager1.add_effect(effects.Dead())
    self.villager2.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.goon1, self.goon2])

  def test_town_wins_with_joker_alive(self):
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.goon1.add_effect(effects.Dead())
    assert_equal(self.game.winners(), NO_WINNER_YET)
    self.goon2.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.villager1, self.villager2, self.villager3])

  def test_usurper_wins(self):
    usurper = self.game.add_player("Usurper", Usurper(self.mafia))
    self.goon1.add_effect(effects.Dead())
    self.goon2.add_effect(effects.Dead())
    self.villager1.add_effect(effects.Dead())
    self.villager2.add_effect(effects.Dead())
    self.villager3.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.goon1, self.goon2, usurper])

  def test_usurper_loses(self):
    usurper = self.game.add_player("Usurper", Usurper(self.mafia))
    self.villager1.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.goon1, self.goon2])

  def test_godfather_alignment(self):
    self.goon1.add_effect(effects.Dead())
    self.goon2.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.villager1, self.villager2, self.villager3])

    godfather = self.game.add_player("Godfather", Godfather(self.mafia))
    assert_equal(self.game.winners(), NO_WINNER_YET)

  def test_town_wins_exclusively(self):
    assert not self.game.is_game_over()
    self.goon1.add_effect(effects.Dead())
    self.goon2.add_effect(effects.Dead())
    assert self.game.is_game_over()

  def test_mafia_wins_exclusively(self):
    assert not self.game.is_game_over()
    self.villager1.add_effect(effects.Dead())
    self.villager2.add_effect(effects.Dead())
    assert self.game.is_game_over()

  def test_joker_undecided(self):
    assert_equal(self.joker.fate(player=self.joker), Fate.undecided)

  def test_joker_wins_non_exclusively(self):
    assert not self.game.is_game_over()
    self.game.log.append(events.Lynched(self.joker))
    self.joker.add_effect(effects.Dead())
    assert_equal(self.game.winners(), [self.joker])
    assert not self.game.is_game_over()

  def test_everyone_loses(self):
    g = TestGame()
    town = g.add_faction(Town())
    villager = g.add_player("Villager", Villager(town))
    villager.add_effect(effects.Dead())
    assert_equal(g.winners(), EVERYONE_LOST)
