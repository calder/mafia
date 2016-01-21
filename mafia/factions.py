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

  def __str__(self):
    return self.__class__.__name__

class Town(Faction):
  alignment = Alignment.good

  def __init__(self):
    super().__init__("Town")

  def fate(self, game):
    good_players = [p for p in game.live_players if p.role.faction.alignment is Alignment.good]
    evil_players = [p for p in game.live_players if p.role.faction.alignment is Alignment.evil]
    if len(good_players) == 0: return Fate.lost
    if len(evil_players) == 0: return Fate.won
    return Fate.undecided

class Mafia(Faction):
  alignment = Alignment.evil

  def __init__(self, name):
    super().__init__(name)
    self.action = Kill(Placeholder.FactionMember(self), Placeholder.AnyPlayer())

  def fate(self, game):
    members = [p for p in game.live_players if p.role.faction is self]
    if len(members) == 0: return Fate.lost
    if 2 * len(members) >= len(game.live_players): return Fate.won
    return Fate.undecided
