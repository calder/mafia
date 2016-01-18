from mafia import *
from .test_game import TestGame

from nose_parameterized import parameterized
from unittest import TestCase

def test_mafia_kill():
  game = TestGame()
  town  = game.add_faction(Town())
  mafia = game.add_faction(Mafia("Mafia"))
  villager = game.add_player(Player("Villager", role=Villager(faction=town)))
  goon     = game.add_player(Player("Goon", role=Goon(faction=mafia)))

  night0 = Night(0)
  night0.add_action(FactionAction(mafia, Kill(goon, villager)))

  assert villager.alive
  game.resolve(night0)
  assert not villager.alive

  assert_equal(game.log, Log([
    Visited(goon, villager),
    Died(villager),
  ], phase=night0))
