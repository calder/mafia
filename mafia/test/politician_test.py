from mafia import *
from .test_game import TestGame

from unittest import TestCase

class PoliticianTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.double_voter = self.game.add_player("Double Voter", Villager(self.town))
    self.goon         = self.game.add_player("Goon", Goon(self.mafia))
    self.roleblocker  = self.game.add_player("Roleblocker", Roleblocker(self.town))
    self.politician   = self.game.add_player("Politician", Politician(self.town))
    self.villager     = self.game.add_player("Villager", Villager(self.town))

  def test_basic_politician(self):
    """Test that a politician can swing someone's vote."""
    night0 = Night(0)
    night0.add_action(StealVote(self.politician, self.villager))
    self.game.resolve(night0)

    day1 = Day(1)
    day1.set_vote(self.goon, self.roleblocker)
    day1.set_vote(self.villager, self.roleblocker)
    day1.set_vote(self.politician, self.goon)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      VotedFor(self.goon, self.roleblocker),
      VotedFor(self.politician, self.goon),
      VotedFor(self.villager, self.goon, original_vote=self.roleblocker),
      Lynched(self.goon),
    ], phase=day1))
    assert self.roleblocker.alive is True
    assert self.goon.alive is False

  def test_politician_death(self):
    """Test that a dead politician blackholes their target's vote."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.politician)))
    night0.add_action(StealVote(self.politician, self.villager))
    self.game.resolve(night0)

    assert self.politician.alive is False

    day1 = Day(1)
    day1.set_vote(self.villager, self.roleblocker)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      # No votes or lynches
    ], phase=day1))
    assert self.roleblocker.alive is True

  def test_constituent_death(self):
    """Test that a politician cannot steal a dead player's vote."""
    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.double_voter)))
    night0.add_action(StealVote(self.politician, self.double_voter))
    self.game.resolve(night0)

    assert self.double_voter.alive is False

    day1 = Day(1)
    day1.set_vote(self.goon, self.roleblocker)
    day1.set_vote(self.politician, self.goon)
    day1.set_vote(self.villager, self.roleblocker)
    self.game.resolve(day1)

    assert_equal(self.game.log.phase(day1), Log([
      VotedFor(self.goon, self.roleblocker),
      VotedFor(self.politician, self.goon),
      VotedFor(self.villager, self.roleblocker),
      Lynched(self.roleblocker),
    ], phase=day1))
    assert self.roleblocker.alive is False
