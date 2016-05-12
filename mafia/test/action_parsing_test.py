from mafia import *
from .test_game import TestGame

from unittest import TestCase

class ActionParsingTest(TestCase):
  def setUp(self):
    self.game = TestGame()
    self.town  = self.game.add_faction(Town())
    self.mafia = self.game.add_faction(Mafia("Mafia"))
    self.godfather = self.game.add_player("Godfather", Godfather(self.mafia))
    self.usurper   = self.game.add_player("Usurper", Usurper(self.mafia))
    self.hitman    = self.game.add_player("Hitman", Hitman(self.mafia))
    self.goon      = self.game.add_player("Goon", Goon(self.mafia))
    self.cop       = self.game.add_player("Cop", Cop(self.town))
    self.doctor    = self.game.add_player("Doctor", Doctor(self.town))
    self.busdriver = self.game.add_player("Busdriver", Busdriver(self.town))
    self.villager  = self.game.add_player("Villager", Villager(self.town))

  def test_night_parsing(self):
    """Test Night action parsing."""
    night0 = Night(0)
    night0.add_parsed(self.godfather, "hitman: hitman kill cop", game=self.game)
    night0.add_parsed(self.doctor, "protect cop", game=self.game)
    with self.assertRaises(NoFactionAction):
      night0.add_parsed(self.villager, "busdriver: kill godfather", game=self.game)
    with self.assertRaises(NoIndividualAction):
      night0.add_parsed(self.villager, "investigate godfather", game=self.game)
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor, self.cop),
      events.Visited(self.hitman, self.cop),
      events.Died(self.cop),
    ], phase=night0))

  def test_day_parsing(self):
    """Test Day vote parsing."""
    day0 = Day(0)
    day0.add_parsed(self.godfather, "vote cop", game=self.game)
    day0.add_parsed(self.cop, "vote for godfather", game=self.game)
    day0.add_parsed(self.usurper, "lynch godfather", game=self.game)
    self.game.resolve(day0)

    assert_equal(self.game.log.phase(day0), Log([
      events.VotedFor(self.cop, self.godfather),
      events.VotedFor(self.godfather, self.cop),
      events.VotedFor(self.usurper, self.godfather),
      events.Lynched(self.godfather),
      events.FactionLeaderAnnouncement(self.mafia, self.usurper),
    ], phase=day0))

  def test_parse_action(self):
    """Test Action parsing."""
    action = self.cop.action.parse("investigate doctor", game=self.game, player=self.cop)
    assert Investigate(self.cop, self.doctor).matches(action, debug=True)

  def test_parse_illegal_action(self):
    """Test illegal Action rejection."""
    with self.assertRaises(IllegalAction):
      self.doctor.action.parse("protect doctor", game=self.game, player=self.doctor)

  def test_action_help(self):
    """Test Action help."""
    assert_equal(self.cop.action.help(), ["investigate PLAYER"])

  def test_parse_busdrive(self):
    """Test Busdrive parsing."""
    action = self.busdriver.action.parse("busdrive cop and godfather", game=self.game, player=self.busdriver)
    assert Busdrive(self.busdriver, self.cop, self.godfather).matches(action, debug=True)

  def test_parse_illegal_busdrive(self):
    """Test illegal Busdrive rejection."""
    self.doctor.add_effect(effects.Dead())
    with self.assertRaises(IllegalAction):
      self.busdriver.action.parse("busdrive cop and doctor", game=self.game, player=self.busdriver)

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
    with self.assertRaises(InvalidSender):
      self.mafia.action.parse("goon: kill cop", game=self.game, player=self.usurper)

    self.godfather.add_effect(effects.Dead())

    action = self.mafia.action.parse("goon: kill cop", game=self.game, player=self.usurper)
    assert FactionAction(self.mafia, Kill(self.goon, self.cop)).matches(action, debug=True)
