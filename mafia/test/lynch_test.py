from mafia import *
from .test_game import TestGame

from unittest import TestCase

class LynchTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.villager3 = self.game.add_player("Villager 3", Villager(self.town))

  def test_basic_lynch(self):
    """Basic voting functionality."""
    day1 = Day(1)
    day1.set_vote(self.villager1, self.villager3)
    day1.set_vote(self.villager2, self.villager3)
    day1.set_vote(self.villager3, self.villager1)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      events.VotedFor(self.villager1, self.villager3),
      events.VotedFor(self.villager2, self.villager3),
      events.VotedFor(self.villager3, self.villager1),
      events.Lynched(self.villager3),
    ], phase=day1))
    assert not self.villager3.alive

  def test_multiple_votes(self):
    """A player should not be able to vote multiple times."""
    day1 = Day(1)
    day1.set_vote(self.villager1, self.villager3)
    day1.set_vote(self.villager2, self.villager3)
    day1.set_vote(self.villager3, self.villager1)
    day1.set_vote(self.villager3, self.villager1)
    day1.set_vote(self.villager3, self.villager1)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      events.VotedFor(self.villager1, self.villager3),
      events.VotedFor(self.villager2, self.villager3),
      events.VotedFor(self.villager3, self.villager1),
      events.Lynched(self.villager3),
    ], phase=day1))
    assert not self.villager3.alive
