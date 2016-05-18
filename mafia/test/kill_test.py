from mafia import *
from .test_game import TestGame

from unittest import TestCase

class KillTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town = self.game.add_faction(Town())
    self.villager   = self.game.add_player("Villager", Villager(self.town))
    self.vigilante1 = self.game.add_player("Vigilante 1", Vigilante(self.town))
    self.vigilante2 = self.game.add_player("Vigilante 2", Vigilante(self.town))
    self.vigilante3 = self.game.add_player("Vigilante 3", Vigilante(self.town))
    self.cop        = self.game.add_player("Cop", Cop(self.town))
    self.tracker    = self.game.add_player("Tracker", Tracker(self.town))
    self.watcher    = self.game.add_player("Watcher", Watcher(self.town))

  def test_double_kill(self):
    """Only the first kill in a given night succeeds."""

    night1 = Night(1)
    night1.add_action(Kill(self.vigilante1, self.villager))
    night1.add_action(Kill(self.vigilante2, self.villager))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.vigilante1, self.villager),
      events.Died(self.villager),
      events.Visited(self.vigilante2, self.villager),
    ], phase=night1))
    assert not self.villager.alive

  def test_kill_investigator(self):
    """Investigative roles should not receive results on the night they die."""

    night1 = Night(1)
    night1.add_action(Kill(self.vigilante1, self.cop))
    night1.add_action(Kill(self.vigilante2, self.tracker))
    night1.add_action(Kill(self.vigilante3, self.watcher))
    night1.add_action(Investigate(self.cop, self.villager))
    night1.add_action(Track(self.tracker, self.villager))
    night1.add_action(Watch(self.watcher, self.villager))
    self.game.resolve(night1)

    assert_equal(self.game.log.phase(night1), Log([
      events.Visited(self.cop, self.villager),
      events.Visited(self.tracker, self.villager),
      events.Visited(self.watcher, self.villager),
      events.Visited(self.vigilante1, self.cop),
      events.Died(self.cop),
      events.Visited(self.vigilante2, self.tracker),
      events.Died(self.tracker),
      events.Visited(self.vigilante3, self.watcher),
      events.Died(self.watcher),
    ], phase=night1))
