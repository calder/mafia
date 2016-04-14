from mafia import *
from .test_game import TestGame

from unittest import TestCase

class EffectTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.goon1     = self.game.add_player("Goon 1", Goon(self.mafia))
    self.goon2     = self.game.add_player("Goon 2", Goon(self.mafia))

  def test_expired_effect(self):
    """Expired effects should appear empty."""
    class TestEffect(Effect): foo = 123

    effect = TestEffect(expiration=Days(1))
    assert hasattr(effect, "foo")

    effect.expiration.advance_day()
    assert not hasattr(effect, "foo")
