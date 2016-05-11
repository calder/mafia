from mafia import *

from unittest import TestCase

class StrTest(TestCase):
  def setUp(self):
    self.town  = Town()
    self.mafia = Mafia("Alliance")
    self.jayne = Player("Jayne", Villager(self.town))
    self.mal   = Player("Mal", Villager(self.town))

  def test_str_nested_role(self):
    ninja_hitman = Ninja(Hitman(self.mafia))
    assert_equal(str(ninja_hitman), "Mafia Ninja Hitman")

  def test_str_player(self):
    assert_equal(str(self.jayne), "Jayne")

  def test_str_action(self):
    class TestAction(Action): pass
    assert_equal(str(TestAction(self.jayne, self.mal)), "TestAction(Jayne, Mal)")

  def test_str_kill(self):
    assert_equal(str(Kill(self.jayne, self.mal)), "Kill(Jayne, Mal)")
    assert_equal(str(HitmanKill(self.jayne, self.mal)), "HitmanKill(Jayne, Mal)")

  def test_str_alignment(self):
    assert_equal(str(Alignment.good), "good")

  def test_str_effect(self):
    class TestEffect(Effect): pass
    assert_equal(str(TestEffect(expiration=Never())), "TestEffect(expiration=Never())")

  def test_expirations(self):
    assert_equal(str(Days(123)), "Days(123)")
    assert_equal(str(Nights(4)), "Nights(4)")

  def test_str_faction(self):
    assert_equal(str(Faction("Blue Sun")), "Blue Sun")

  def test_role_announcement_full_message(self):
    sue = Player("Sue", Doctor(Ninja(Hitman(self.mafia))))
    sue.role.description = "Doctor stuff..."
    sue.role.base.description = "Ninja stuff..."
    sue.role.base.base.description = "Hitman stuff..."
    announcement = events.RoleAnnouncement(sue, sue.role)
    self.assertEqual(
      announcement.full_message,
      "You are the Mafia Doctor Ninja Hitman.\n\n" \
      "Doctor stuff...\n\nNinja stuff...\n\nHitman stuff...\n\n" \
      "---------------------------------------\n" \
      "You may send me the following commands:\n" \
      "- protect PLAYER"
    )
