from .actions import *
from .alignment import *
from . import placeholders
from .util import *
from .virtual_actions import *

import enum

class Fate(enum.Enum):
  won       = 1
  lost      = 2
  undecided = 3

class Faction(object):
  wins_exclusively  = True
  secret_membership = False

  def __init__(self, name):
    self.name = name

  def __lt__(self, other):
    return self.name < other.name

  def __str__(self):
    return self.name

  def leader(self, *, game):
    members = [p for p in game.player_list if p.faction == self and p.alive]
    return members[0] if len(members) > 0 else None

  def members(self, *, game):
    return [p for p in game.players if p.faction == self]

  def all_members(self, *, game):
    return [p for p in game.all_players if p.faction == self]

  def action(self, *, game):
    member_actions = [p.faction_action for p in self.members(game=game) if p.faction_action]
    if member_actions: return FactionAction(self, OneOfAction(member_actions))

class Town(Faction):
  adjective         = "Town"
  alignment         = Alignment.good
  objective         = "You win if all the mafia are eliminated."
  secret_membership = True

  def __init__(self):
    super().__init__("Town")

  def fate(self, *, game, **kwargs):
    good_players = len([p for p in game.players if p.alignment == Alignment.good])
    evil_players = len([p for p in game.players if p.alignment == Alignment.evil])
    if good_players == 0: return Fate.lost
    if evil_players == 0: return Fate.won
    return Fate.undecided

class Mafia(Faction):
  adjective = "Mafia"
  alignment = Alignment.evil
  objective = "You win if you outnumber all other players in the game."

  def fate(self, *, game, **kwargs):
    members = self.members(game=game)
    if len(members) == 0: return Fate.lost
    if len(members) > len(game.players) / 2: return Fate.won
    return Fate.undecided

class Masonry(Faction):
  adjective = "Mason"
  alignment = Alignment.good
  objective = Town.objective

  def __init__(self, name, town):
    super().__init__(name)
    self.town = town

  @property
  def alignment(self):
    return self.town.alignment

  def fate(self, **kwargs):
    return self.town.fate(**kwargs)

class ThirdParty(Faction):
  adjective = "Third-Party"
  secret_membership = True
