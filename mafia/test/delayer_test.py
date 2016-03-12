from mafia import *
from .test_game import TestGame

from unittest import TestCase

class DelayerTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.delayer       = self.game.add_player("Delayer", Delayer(self.town))
    self.cop           = self.game.add_player("Cop", Cop(self.town))
    self.roleblocker   = self.game.add_player("Roleblocker", Roleblocker(self.town))
    self.ventriloquist = self.game.add_player("Ventriloquist", Ventriloquist(self.town))

  def test_basic_delayer(self):
    """Test that a delayer can delay actions."""
    night0 = Night(0)
    night0.add_action(Investigate(self.cop, self.roleblocker))
    night0.add_action(Delay(self.delayer, self.cop))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.delayer, self.cop),
      events.Delayed(self.cop),
    ], phase=night0))

    self.game.resolve(Day(1))

    night1 = Night(1)
    night1.add_action(Investigate(self.cop, self.ventriloquist))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.cop, self.roleblocker),
      events.InvestigationResult(Alignment.good, target=self.roleblocker, to=self.cop),
      events.Visited(self.cop, self.ventriloquist),
      events.InvestigationResult(Alignment.good, target=self.ventriloquist, to=self.cop),
    ], phase=night1))
