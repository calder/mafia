from mafia import *

import unittest

class RoleblockingTest(unittest.TestCase):
  def setUp(self):
    self.game = Game()
    self.game.log.on_append(lambda event: print(event.colored_str()))
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager    = self.game.add_player(Player("Villager", role=Villager(faction=self.town)))
    self.goon        = self.game.add_player(Player("Goon", role=Goon(faction=self.mafia)))
    self.roleblocker = self.game.add_player(Player("Roleblocker", role=Roleblocker(faction=self.town)))

  def test_basic_roleblocking(self):
    """Test that a basic kill action can be roleblocked."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Roleblock(self.roleblocker, self.goon))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      Visited(self.roleblocker, self.goon),
      Blocked(self.goon),
    ], phase=night0))
    assert self.villager.alive

  def test_watcher_roleblocking(self):
    """
    Test that watchers can be roleblocked.

    Watch actions are resolved in resolve_post, after other night actions.
    """
    night0 = Night(0)
    watcher = self.game.add_player(Player("Watcher", role=Watcher(faction=self.town)))
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Watch(watcher, self.villager))
    night0.add_action(Roleblock(self.roleblocker, watcher))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      Visited(self.roleblocker, watcher),
      Visited(self.goon, self.villager),
      Died(self.villager),
      Blocked(watcher),
    ], phase=night0))
