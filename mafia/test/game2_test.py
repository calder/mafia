from mafia import *
from .test_game import TestGame

from unittest import TestCase

def test_game2():
  g = TestGame()
  town  = g.add_faction(Town())
  mafia = g.add_faction(Mafia("NSA"))
  alice  = g.add_player("Alice", Villager(town))
  bob    = g.add_player("Bob", Villager(town))
  eve    = g.add_player("Eve", Godfather(mafia))
  malory = g.add_player("Malory", Goon(mafia))

  night0 = Night(0)
  night0.add_action(FactionAction(mafia, Kill(malory, alice)))
  g.resolve(night0)
