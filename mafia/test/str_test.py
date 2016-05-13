from mafia import *
from .test_game import *

from unittest import TestCase

class StrTest(TestCase):
  def setUp(self):
    self.maxDiff = None

    self.game  = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Alliance"))
    self.jayne = self.game.add_player("Jayne", Villager(self.town))
    self.mal   = self.game.add_player("Mal", Villager(self.town))
    self.hob1  = self.game.add_player("HoB 1", Hitman(self.mafia))
    self.hob2  = self.game.add_player("HoB 2", Goon(self.mafia))

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

  def test_faction_leader_announcement_message(self):
    announcement = events.FactionLeaderAnnouncement(self.mafia, self.hob1)
    announcement.phase = START
    self.assertEqual(announcement.message, "You are the leader of the Alliance.")

  def test_faction_leader_announcement_full_message(self):
    announcement = events.FactionLeaderAnnouncement(self.mafia, self.hob1)
    self.assertEqual(
      announcement.full_message,
      "You are now the leader of the Alliance.\n\n" \
      "---------------------------------------\n" \
      "You may send me the following commands:\n" \
      "  hob1: hitman kill PLAYER\n" \
      "  hob2: kill PLAYER"
    )

  def test_role_announcement_full_message(self):
    sue = Player("Sue", Doctor(Ninja(Hitman(self.mafia))))
    sue.role.description = "Doctor stuff..."
    sue.role.base.description = "Ninja stuff..."
    sue.role.base.base.description = "Hitman stuff..."
    announcement = events.RoleAnnouncement(sue, sue.role)
    self.assertEqual(
      announcement.full_message,
      "You are now the Mafia Doctor Ninja Hitman.\n\n" \
      "Doctor stuff...\n\nNinja stuff...\n\nHitman stuff...\n\n" \
      "You win if your mafia accounts for half or more of the surviving players.\n\n" \
      "---------------------------------------\n" \
      "You may send me the following commands:\n" \
      "  protect PLAYER\n" \
      "  vote for PLAYER\n" \
      "  unvote"
    )
