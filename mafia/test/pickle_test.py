import pickle
from unittest import TestCase

from mafia import *

class PickleTest(TestCase):
  def test_pickle_game(self):
    game      = Game()
    town      = game.add_faction(Town())
    mafia     = game.add_faction(Mafia("Mafia"))
    villager1 = game.add_player("Villager 1", Villager(town))
    villager2 = game.add_player("Villager 2", Villager(town))
    villager3 = game.add_player("Villager 3", Villager(town))
    goon      = game.add_player("Goon", Goon(mafia))

    night0 = Night(0)
    night0.add_action(FactionAction(mafia, Kill(goon, villager1)))
    game.resolve(night0)

    day1 = Day(1)
    day1.set_vote(goon, villager2)
    game.resolve(day1)

    pickled   = pickle.dumps(game)
    game      = pickle.loads(pickled)
    town      = [f for f in game.factions if f.name == "Town"][0]
    mafia     = [f for f in game.factions if f.name == "Mafia"][0]
    villager1 = [p for p in game.all_players if p.name == "Villager 1"][0]
    villager2 = [p for p in game.all_players if p.name == "Villager 2"][0]
    villager3 = [p for p in game.all_players if p.name == "Villager 3"][0]
    goon      = [p for p in game.all_players if p.name == "Goon"][0]
    night0    = game.log[0].phase
    day1      = game.log[2].phase

    night1 = Night(1)
    night1.add_action(FactionAction(mafia, Kill(goon, villager3)))
    game.resolve(night1)

    assert_equal(game.log, Log([
      events.Visited(goon, villager1),
      events.Died(villager1),
    ], phase=night0) + Log([
      events.VotedFor(goon, villager2),
      events.Lynched(villager2),
    ], phase=day1) + Log([
      events.Visited(goon, villager3),
      events.Died(villager3),
    ], phase=night1))

  def test_pickle_singleton_value(self):
    original1 = SingletonValue("SINGLETON", 123)
    original2 = SingletonValue("SINGLETON", 456)
    restored1 = pickle.loads(pickle.dumps(original1))
    restored2 = pickle.loads(pickle.dumps(original2))
    assert_equal(original1, restored1)
    assert_equal(original2, restored2)
    assert restored1 != restored2
