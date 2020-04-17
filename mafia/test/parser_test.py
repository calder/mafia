from mafia import *
from .util import *

from unittest import TestCase

DEFAULT_COMMANDS = [
    "vote PLAYER",
    "set will: ...",
    "help",
]

class ParserTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
    self.town   = self.game.add_faction(Town())
    self.mafia  = self.game.add_faction(Mafia("Mafia"))
    self.villager1 = self.game.add_player("Villager 1", Villager(self.town))
    self.villager2 = self.game.add_player("Villager 2", Villager(self.town))
    self.cop       = self.game.add_player("Cop", Cop(self.town))
    self.goon1     = self.game.add_player("Goon 1", Goon(self.mafia))
    self.goon2     = self.game.add_player("Goon 2", Goon(self.mafia))
    self.joker     = self.game.add_player("Joker", Joker())

    self.parser = Parser(self.game)

  def test_default_commands(self):
    assert [c.help for c in self.parser.get_commands(self.villager1)] == DEFAULT_COMMANDS

  def test_action(self):
    assert [c.help for c in self.parser.get_commands(self.cop)] == [
        "investigate PLAYER",
    ] + DEFAULT_COMMANDS

  def test_faction_action(self):
    assert [c.help for c in self.parser.get_commands(self.goon1)] == [
        "goon 1: kill PLAYER",
        "goon 2: kill PLAYER",
    ] + DEFAULT_COMMANDS
