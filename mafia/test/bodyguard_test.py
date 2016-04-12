from mafia import *
from .test_game import TestGame

from nose_parameterized import parameterized
from unittest import TestCase

class BodyguardTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.goon      = self.game.add_player("Goon", Goon(self.mafia))
    self.villager  = self.game.add_player("Villager", Villager(self.town))
    self.bodyguard = self.game.add_player("Bodyguard", Bodyguard(self.town))
    self.elite     = self.game.add_player("Elite Bodyguard", EliteBodyguard(self.town))
    self.doctor    = self.game.add_player("Doctor", Doctor(self.town))


  @parameterized.expand([(True,), (False,)])
  def test_bodyguard(self, elite):
    """Test basic bodyguard functionality."""

    bodyguard = self.elite if elite else self.bodyguard

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(bodyguard, self.villager, elite=elite))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(bodyguard, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Died(bodyguard),
    ] + ([events.Died(self.goon)] if elite else []), phase=night0))

    assert self.villager.alive is True
    assert bodyguard.alive is False
    assert self.goon.alive is (not elite)


  def test_doctor_target(self):
    """Test that protecting a bodyguard's target doesn't save the bodyguard."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(self.bodyguard, self.villager))
    night0.add_action(Protect(self.doctor, self.villager))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.bodyguard, self.villager),
      events.Visited(self.doctor, self.villager),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Died(self.bodyguard),
    ], phase=night0))

    assert self.villager.alive is True
    assert self.bodyguard.alive is False


  def test_doctor_bodyguard(self):
    """Test that a sacrificial bodyguard can still be protected."""

    night0 = Night(0)
    night0.add_action(FactionAction(self.mafia, Kill(self.goon, self.villager)))
    night0.add_action(Guard(self.bodyguard, self.villager))
    night0.add_action(Protect(self.doctor, self.bodyguard))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.bodyguard, self.villager),
      events.Visited(self.doctor, self.bodyguard),
      events.Visited(self.goon, self.villager),
      events.Protected(self.villager),
      events.Protected(self.bodyguard),
    ], phase=night0))

    assert self.villager.alive is True
    assert self.bodyguard.alive is True

