from .actions import *
from .virtual_actions import *
from .placeholders import *

import enum

Alignment = enum.Enum("Alignment", ["GOOD", "NEUTRAL", "EVIL"])
Fate = enum.Enum("Fate", ["WON", "LOST", "UNDECIDED"])

class Faction(object):
  action = NoAction()

  def __init__(self, name):
    self.name = name

  def __str__(self):
    return self.__class__.__name__

class Town(Faction):
  alignment = Alignment.GOOD

  def __init__(self):
    super().__init__("Town")

  def fate(self, game):
    good_players = [p for p in game.live_players if p.role.faction.alignment is Alignment.GOOD]
    evil_players = [p for p in game.live_players if p.role.faction.alignment is Alignment.EVIL]
    if len(good_players) == 0: return Fate.LOST
    if len(evil_players) == 0: return Fate.WON
    return Fate.UNDECIDED

class Mafia(Faction):
  alignment = Alignment.EVIL

  def __init__(self, name):
    super().__init__(name)
    self.action = Kill(Placeholder.FactionMember(self), Placeholder.Player())

  def fate(self, game):
    members = [p for p in game.live_players if p.role.faction is self]
    if len(members) == 0: return Fate.LOST
    if 2 * len(members) >= len(game.live_players): return Fate.WON
    return Fate.UNDECIDED
