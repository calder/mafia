from .test_game import *
from mafia import *

def test_overeager():
  """Test that an Overeager role has a compelled action."""
  g = TestGame()
  town = g.add_faction(Town())
  villager  = g.add_player("Villager", Villager(town))
  vigilante = g.add_player("Vigilante", Overeager(Vigilante(town)))

  night0 = Night(0)
  g.resolve(night0)
  assert (not villager.alive) or (not vigilante.alive)

def test_overeager_villager():
  """Test that an Overeager Villager doesn't break everything."""
  g = TestGame()
  town = g.add_faction(Town())
  eager_villager = g.add_player("Villager", Overeager(Villager(town)))

  night0 = Night(0)
  g.resolve(night0)
