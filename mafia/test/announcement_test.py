from mafia import *
from .test_game import TestGame

from unittest import TestCase

class AnnouncementTest(TestCase):
  def test_begin(self):
    game  = TestGame()
    mafia = game.add_faction(Mafia("Mafia"))
    goon  = game.add_player("Goon", Goon(mafia))
    game.begin()

    assert_equal(game.log, Log([
      events.RoleAnnouncement(goon, goon.role),
      events.FactionLeaderAnnouncement(mafia, goon),
    ], phase=START))
