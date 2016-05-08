from mafia import *
from .test_game import TestGame

from unittest import TestCase

class ActionParsingTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.cop    = self.game.add_player("Cop", Cop(self.town))
    self.doctor = self.game.add_player("Doctor", Doctor(self.town))

  def test_parse_action(self):
    action = self.cop.action.parse("investigate doctor", game=self.game, player=self.cop)
    assert Investigate(self.cop, self.doctor).matches(action, debug=True)
