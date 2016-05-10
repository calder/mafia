from mafia import *
from .test_game import TestGame

from unittest import TestCase

class ActionParsingTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.godfather = self.game.add_player("Godfather", Godfather(self.mafia))
    self.usurper   = self.game.add_player("Usurper", Usurper(self.mafia, self.godfather))
    self.hitman    = self.game.add_player("Hitman", Hitman(self.mafia))
    self.goon      = self.game.add_player("Goon", Goon(self.mafia))
    self.cop       = self.game.add_player("Cop", Cop(self.town))
    self.doctor    = self.game.add_player("Doctor", Doctor(self.town))
    self.busdriver = self.game.add_player("Busdriver", Busdriver(self.town))

  def test_parse_action(self):
    """Test normal action parsing."""
    action = self.cop.action.parse("investigate doctor", game=self.game, player=self.cop)
    assert Investigate(self.cop, self.doctor).matches(action, debug=True)

  def test_action_help(self):
    """Test normal action help."""
    assert_equal(self.cop.action.help(), ["investigate PLAYER"])

  def test_parse_busdrive(self):
    """Test Busdrive parsing."""
    action = self.busdriver.action.parse("busdrive cop and godfather", game=self.game, player=self.busdriver)
    assert Busdrive(self.busdriver, self.cop, self.godfather).matches(action, debug=True)

  def test_busdrive_help(self):
    """Test Busdrive help."""
    assert_equal(self.busdriver.action.help(), ["busdrive PLAYER1 PLAYER2"])

  def test_parse_faction_action(self):
    """Test FactionAction parsing."""
    action = self.mafia.action.parse("goon: kill cop", game=self.game, player=self.godfather)
    assert FactionAction(self.mafia, Kill(self.goon, self.cop)).matches(action, debug=True)

  def test_faction_action_help(self):
    """Test FactionAction help."""
    assert_equal(self.mafia.action.help(), [
      "godfather: kill PLAYER",
      "goon: kill PLAYER",
      "hitman: hitman kill PLAYER",
      "usurper: kill PLAYER",
    ])

  def test_chain_of_command(self):
    """The chain of command should be the order players were added in."""
    with self.assertRaises(InvalidAction):
      self.mafia.action.parse("goon: kill cop", game=self.game, player=self.usurper)

    self.godfather.add_effect(effects.Dead())

    action = self.mafia.action.parse("goon: kill cop", game=self.game, player=self.usurper)
    assert FactionAction(self.mafia, Kill(self.goon, self.cop)).matches(action, debug=True)
