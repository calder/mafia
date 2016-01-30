from .actions import *
from .alignment import *
from .virtual_actions import *
from .placeholders import *

import enum

class Fate(enum.Enum):
  won       = 1
  lost      = 2
  undecided = 3

class Faction(object):
  action = None

  def __init__(self, name):
    self.name = name

  def __lt__(self, other):
    return self.name < other.name

  def members(self, players):
    return [p for p in players if p.faction == self]

  def apparent_members(self, players):
    return [p for p in players if self in p.apparent_factions]

class Town(Faction):
  adjective = "Town"
  alignment = Alignment.good

  def __init__(self):
    super().__init__("Town")

  def fate(self, players):
    good_players = [p for p in players if p.alignment is Alignment.good]
    evil_players = [p for p in players if p.alignment is Alignment.evil]
    if len(good_players) == 0: return Fate.lost
    if len(evil_players) == 0: return Fate.won
    return Fate.undecided

  def apparent_members(self, players):
    return None

class Mafia(Faction):
  adjective = "Mafia"
  alignment = Alignment.evil

  def __init__(self, name):
    super().__init__(name)
    self.action = Kill(Placeholder.FactionMember(self), Placeholder.Player())

  def fate(self, players):
    members = self.members(players)
    if len(members) == 0: return Fate.lost
    if 2 * len(members) >= len(players): return Fate.won
    return Fate.undecided

class Masonry(Faction):
  adjective = "Mason"
  alignment = Alignment.good

  def __init__(self, name, town):
    super().__init__(name)
    self.town = town

  @property
  def alignment(self):
      return self.town.alignment

  def fate(self, players):
    return self.town.fate
