from mafia import *
from .util import *

from unittest import TestCase

class BodyguardTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.goon      = self.game.add_player("Goon", Goon(self.mafia))
    self.villager  = self.game.add_player("Villager", Villager(self.town))
    self.bodyguard = self.game.add_player("Bodyguard", Bodyguard(self.town))
    self.elite     = self.game.add_player("Elite Bodyguard", EliteBodyguard(self.town))
    self.doctor    = self.game.add_player("Doctor", Doctor(self.town))

  def test_bodyguard(self):
    """Test Bodyguard functionality."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(self.bodyguard, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.bodyguard, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Died(self.bodyguard),
    ], phase=night0))

    assert self.villager.alive
    assert not self.bodyguard.alive
    assert self.goon.alive

  def test_bodyguard(self):
    """Test Elite Bodyguard functionality."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(EliteGuard(self.elite, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.elite, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Died(self.elite),
      events.Died(self.goon),
    ], phase=night0))

    assert self.villager.alive
    assert not self.elite.alive
    assert not self.goon.alive

  def test_doctor_target(self):
    """Test that protecting a bodyguard's target doesn't save the bodyguard."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(self.bodyguard, self.villager))
    night0.add_action(Protect(self.doctor, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor, self.villager),
      events.Visited(self.bodyguard, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Died(self.bodyguard),
    ], phase=night0))

    assert self.villager.alive
    assert not self.bodyguard.alive

  def test_doctor_bodyguard(self):
    """Test that a sacrificial bodyguard can still be protected."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(self.bodyguard, self.villager))
    night0.add_action(Protect(self.doctor, self.bodyguard))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor, self.bodyguard),
      events.Visited(self.bodyguard, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Protected(self.bodyguard),
      events.NoDeaths(),
    ], phase=night0))

    assert self.villager.alive
    assert self.bodyguard.alive

