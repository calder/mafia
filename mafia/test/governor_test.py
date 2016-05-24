from mafia import *
from .util import *

from unittest import TestCase

class GovernorTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
    self.town  = self.game.add_faction(Town())
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.governor  = self.game.add_player("Governor", Governor(self.town))

  def test_basic_governor(self):
    """Test that a governor can save someone."""
    day1 = Day(1)
    day1.set_vote(self.villager1, self.villager2)
    day1.set_vote(self.governor, self.villager2)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      events.VotedFor(self.governor, self.villager2),
      events.VotedFor(self.villager1, self.villager2),
      events.NoLynch(),
    ], phase=day1))
    assert self.villager2.alive

  def test_governor_self_pardon(self):
    """Test that a governor cannot save themselves."""
    day1 = Day(1)
    day1.set_vote(self.governor, self.governor)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      events.VotedFor(self.governor, self.governor),
      events.Lynched(self.governor),
    ], phase=day1))
    assert not self.governor.alive
