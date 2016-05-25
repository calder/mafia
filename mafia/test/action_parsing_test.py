from mafia import *
from .util import *

from unittest import TestCase

class ActionParsingTest(TestCase):
  def setUp(self):
    self.game = LoggingGame()
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

    self.parser = Parser(self.game)

  def test_night_parsing(self):
    """Test Night action parsing."""
    night0 = Night(0)
    self.parser.parse(night0, self.godfather, "hitman: hitman kill cop")
    self.parser.parse(night0, self.doctor, "protect cop")
    with self.assertRaises(InvalidAction):
      self.parser.parse(night0, self.villager, "busdriver: kill godfather")
    with self.assertRaises(InvalidAction):
      self.parser.parse(night0, self.villager, "investigate godfather")
    self.game.resolve(night0)

    assert_equal(self.game.log.phase(night0), Log([
      events.Visited(self.doctor, self.cop),
      events.Visited(self.hitman, self.cop),
      events.Died(self.cop),
    ], phase=night0))

  def test_day_parsing(self):
    """Test Day vote parsing."""
    day0 = Day(0)
    self.parser.parse(day0, self.hitman, "vote cop")
    self.parser.parse(day0, self.godfather, "vote cop")
    self.parser.parse(day0, self.cop, "vote godfather")
    self.parser.parse(day0, self.usurper, "lynch godfather")
    self.parser.parse(day0, self.hitman, "unvote")
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
    night0 = Night(0)
    self.parser.parse(night0, self.cop, "investigate doctor")
    assert Investigate(self.cop, self.doctor).matches(night0.raw_actions[0], debug=True)

  def test_parse_illegal_action(self):
    """Test illegal Action rejection."""
    with self.assertRaises(IllegalAction):
      self.parser.parse(Night(0), self.doctor, "protect doctor")

  def test_action_help(self):
    """Test Action help."""
    assert_contains("investigate PLAYER", self.parser.get_help(self.cop))

  def test_parse_busdrive(self):
    """Test Busdrive parsing."""
    night0 = Night(0)
    self.parser.parse(night0, self.busdriver, "busdrive cop godfather")
    assert Busdrive(self.busdriver, self.cop, self.godfather).matches(night0.raw_actions[0], debug=True)

  def test_parse_illegal_busdrive(self):
    """Test illegal Busdrive rejection."""
    self.doctor.add_effect(effects.Dead())
    with self.assertRaises(IllegalAction):
      self.parser.parse(Night(0), self.busdriver, "busdrive cop doctor")

  def test_busdrive_help(self):
    """Test Busdrive help."""
    assert_contains("busdrive PLAYER PLAYER", self.parser.get_help(self.busdriver))

  def test_parse_faction_action(self):
    """Test FactionAction parsing."""
    night0 = Night(0)
    self.parser.parse(night0, self.godfather, "goon: kill cop")
    assert FactionAction(self.mafia, Kill(self.goon, self.cop)).matches(night0.raw_actions[0], debug=True)

  def test_faction_action_help(self):
    """Test FactionAction help."""
    help = self.parser.get_help(self.godfather)
    assert_contains("godfather: kill PLAYER", help)
    assert_contains("goon: kill PLAYER", help)
    assert_contains("hitman: hitman kill PLAYER", help)
    assert_contains("usurper: kill PLAYER", help)

  def test_chain_of_command(self):
    """The chain of command should be the order players were added in."""
    with self.assertRaises(InvalidAction):
      self.parser.parse(Night(0), self.usurper, "goon: kill cop")

    self.godfather.add_effect(effects.Dead())

    night0 = Night(0)
    self.parser.parse(night0, self.usurper, "goon: kill cop")
    assert FactionAction(self.mafia, Kill(self.goon, self.cop)).matches(night0.raw_actions[0], debug=True)

  def test_wrong_phase(self):
    # Off-phase vote
    with self.assertRaises(WrongPhase):
      self.parser.parse(Night(0), self.godfather, "vote cop")

    # Off-phase action
    with self.assertRaises(WrongPhase):
      self.parser.parse(Day(1), self.cop, "investigate godfather")

    # Off-phase faction action
    with self.assertRaises(WrongPhase):
      self.parser.parse(Day(1), self.godfather, "goon: kill cop")

  def test_help(self):
    with self.assertRaises(HelpRequested):
      self.parser.parse(Night(0), self.godfather, "help")
