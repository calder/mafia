from mafia import *
from .test_game import TestGame

from nose_parameterized import parameterized
from unittest import TestCase

class RoleblockingTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager    = self.game.add_player("Villager", Villager(self.town))
    self.goon        = self.game.add_player("Goon", Goon(self.mafia))
    self.roleblocker = self.game.add_player("Roleblocker", Roleblocker(self.town))

  @parameterized.expand([(True,), (False,)])
  def test_basic_roleblocking(self, roleblock):
    """Test that a basic kill action can be roleblocked."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    if roleblock: night0.add_action(Roleblock(self.roleblocker, self.goon))
    self.game.resolve(night0)

    assert self.villager.alive is roleblock
    if roleblock:
      assert_equal(self.game.log, Log([
        Visited(self.roleblocker, self.goon),
        Blocked(self.goon),
      ], phase=night0))
    else:
      assert_equal(self.game.log, Log([
        Visited(self.goon, self.villager),
        Died(self.villager),
      ], phase=night0))

  @parameterized.expand([(True,), (False,)])
  def test_watcher_roleblocking(self, roleblock):
    """
    Test that watchers can be roleblocked.

    Watch actions are resolved in resolve_post, after other night actions.
    """
    night0 = Night(0)
    watcher = self.game.add_player("Watcher", Watcher(self.town))
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Watch(watcher, self.villager))
    if roleblock: night0.add_action(Roleblock(self.roleblocker, watcher))
    self.game.resolve(night0)

    if roleblock:
      assert_equal(self.game.log, Log([
        Visited(self.roleblocker, watcher),
        Visited(self.goon, self.villager),
        Died(self.villager),
        Blocked(watcher),
      ], phase=night0))
    else:
      assert_equal(self.game.log, Log([
        Visited(self.goon, self.villager),
        Died(self.villager),
        Visited(watcher, self.villager),
        SawVisitor(self.goon, to=watcher),
      ], phase=night0))
