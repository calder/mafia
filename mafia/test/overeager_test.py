from .util import *
from mafia import *

def test_overeager():
  """Test that an Overeager role has a compelled action."""
  g = LoggingGame()
  town = g.add_faction(Town())
  villager  = g.add_player("Villager", Villager(town))
  vigilante = g.add_player("Vigilante", Overeager(Vigilante(town)))

  night0 = Night(0)
  g.resolve(night0)
  assert (not villager.alive) or (not vigilante.alive)

def test_overeager_villager():
  """Test that an Overeager Villager doesn't break everything.

  This is important because Overeager players could somehow lose
  their action, and we don't want the game to break.
  """
  g = LoggingGame()
  town = g.add_faction(Town())
  villager_role = Villager(town)
  villager_role.action = 123
  eager_villager = g.add_player("Villager", Overeager(villager_role))
  del villager_role.action

  night0 = Night(0)
  g.resolve(night0)
