from mafia import *
from .util import *

from unittest import TestCase

class RoleblockerTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager    = self.game.add_player("Villager", Villager(self.town))
    self.goon        = self.game.add_player("Goon", Goon(self.mafia))
    self.roleblocker = self.game.add_player("Roleblocker", Roleblocker(self.town))

  def test_basic_roleblocking(self):
    """Test that a basic kill action can be roleblocked."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Roleblock(self.roleblocker, self.goon))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      events.Visited(self.roleblocker, self.goon),
      events.Blocked(self.goon),
      events.NoDeaths(),
    ], phase=night0))
    assert self.villager.alive

  def test_roleblocking_expires(self):
    """Test that target is only roleblocked for one night."""
    night0 = Night(0)
    night0.add_action(Roleblock(self.roleblocker, self.goon))
    self.game.resolve(night0)

    self.game.resolve(Day(1))

    night1 = Night(1)
    night1.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    self.game.resolve(night1)

    assert not self.villager.alive
    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.goon, self.villager),
      events.Died(self.villager),
    ], phase=night1))

  def test_watcher_roleblocking(self):
    """
    Test that watchers can be roleblocked.

    Watch actions are resolved in resolve_post, after other night actions.
    """
    night0 = Night(0)
    watcher = self.game.add_player("Watcher", Watcher(self.town))
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Watch(watcher, self.villager))
    night0.add_action(Roleblock(self.roleblocker, watcher))
    self.game.resolve(night0)

    assert_equal(self.game.log, Log([
      events.Visited(self.roleblocker, watcher),
      events.Blocked(watcher),
      events.Visited(self.goon, self.villager),
      events.Died(self.villager),
    ], phase=night0))
