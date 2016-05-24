from mafia import *
from .util import *

from unittest import TestCase

class AnnouncementTest(TestCase):
  def test_begin(self):
    game  = LoggingGame()
    mafia = game.add_faction(Mafia("Mafia"))
    goon  = game.add_player("Goon", Goon(mafia))
    game.begin()

    assert_equal(game.log, Log([
      events.RoleAnnouncement(goon, goon.role),
      events.FactionLeaderAnnouncement(mafia, goon),
    ], phase=START))
