from mafia import *

from unittest import TestCase

class StrTest(TestCase):
  def test_nested_role(self):
    mafia = Mafia("The Sopranos")
    ninja_hitman = Ninja(Hitman(mafia))
    assert_equal(str(ninja_hitman), "Mafia Ninja Hitman")

  def test_kill(self):
    town = Town()
    jayne = Player("Jayne", Villager(town))
    mal   = Player("Mal", Villager(town))
    assert_equal(str(Kill(jayne, mal)), "Kill(Jayne, Mal)")
    assert_equal(str(Kill(jayne, mal, protectable=False)), "Hitman Kill(Jayne, Mal)")
