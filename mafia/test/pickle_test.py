import pickle
from unittest import TestCase

from mafia import *

class PickleTest(TestCase):
  def test_game_pickle(self):
    game     = Game()
    town     = game.add_faction(Town())
    mafia    = game.add_faction(Mafia("Mafia"))
    villager = game.add_player("Villager", Villager(town))
    goon     = game.add_player("Goon", Goon(mafia))

    pickled  = pickle.dumps(game)
    game     = pickle.loads(pickled)
    town     = game.faction_dict["Town"]
    mafia    = game.faction_dict["Mafia"]
    villager = game.player_dict["Villager"]
    goon     = game.player_dict["Goon"]

    night0 = Night(0)
    night0.add_action(FactionAction(mafia, Kill(goon, villager)))
    game.resolve(night0)

    assert_equal(game.log.phase(night0), Log([
      events.Visited(goon, villager),
      events.Died(villager),
    ], phase=night0))
