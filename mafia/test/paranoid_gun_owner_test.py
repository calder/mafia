from mafia import *
from .util import *

from unittest import TestCase

class ParanoidGunOwnerTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
    self.town = self.game.add_faction(Town())
    self.gun_owner = self.game.add_player("Paranoid Gun Owner", ParanoidGunOwner(self.town))
    self.bodyguard = self.game.add_player("Bodyguard", Bodyguard(self.town))
    self.doctor1   = self.game.add_player("Doctor 1", Doctor(self.town))
    self.doctor2   = self.game.add_player("Doctor 2", Doctor(self.town))

  def test_paranoid_gun_owner_visited(self):
    """Test that a Paranoid Gun Owner's kills visitors."""

    night0 = Night(0)
    night0.add_action(Protect(self.doctor1, self.gun_owner))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor1, self.gun_owner),
      events.Died(self.doctor1),
    ], phase=night0))
    assert not self.doctor1.alive

  def test_paranoid_gun_owner_is_protectable(self):
    """Test that a Paranoid Gun Owner's kill is protectable.

    To be a proper test, the action must ordinarily resolve before the
    victim protection. A second Protection is perfect for this.
    """

    night0 = Night(0)
    night0.add_action(Protect(self.doctor1, self.gun_owner))
    night0.add_action(Protect(self.doctor2, self.doctor1))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor2, self.doctor1),
      events.Visited(self.doctor1, self.gun_owner),
      events.Protected(self.doctor1),
      events.NoDeaths(),
    ], phase=night0))
    assert self.doctor1.alive

  def test_paranoid_gun_owner_is_bodyguardable(self):
    """Test that a Paranoid Gun Owner's kill is Bodyguardable."""

    night0 = Night(0)
    night0.add_action(Protect(self.doctor1, self.gun_owner))
    night0.add_action(Guard(self.bodyguard, self.doctor1))
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.bodyguard, self.doctor1),
      events.Visited(self.doctor1, self.gun_owner),
      events.Protected(self.doctor1),
      events.Died(self.bodyguard),
    ], phase=night0))
    assert self.doctor1.alive
    assert not self.bodyguard.alive
