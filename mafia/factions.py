from .actions import *
from .alignment import *
from .virtual_actions import *
from . import placeholders

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
    self.game = None

  def __lt__(self, other):
    return self.name < other.name

  def __str__(self):
    return self.name

  @property
  def leader(self):
    members = [p for p in self.game.player_list if p.faction == self and p.alive]
    return members[0] if len(members) > 0 else None

  @property
  def members(self):
    return [p for p in self.game.players if p.faction == self]

  @property
  def all_members(self):
    return [p for p in self.game.all_players if p.faction == self]

  @property
  def action(self):
    member_actions = [p.faction_action for p in self.members if p.faction_action]
    if member_actions: return FactionAction(self, OneOfAction(member_actions))

class Town(Faction):
  adjective         = "Town"
  alignment         = Alignment.good
  is_town_friend    = True
  is_town_enemy     = False
  objective         = "You win if all the mafia are eliminated."
  secret_membership = True

  def __init__(self):
    super().__init__("Town")

  def fate(self, **kwargs):
    town_friends = [p for p in self.game.players if p.is_town_friend]
    town_enemies = [p for p in self.game.players if p.is_town_enemy]
    if len(town_friends) == 0: return Fate.lost
    if len(town_enemies) == 0: return Fate.won
    return Fate.undecided

class JokerFaction(Faction):
  adjective        = "Third Party"
  alignment        = Alignment.evil
  is_town_enemy    = False
  is_town_friend   = False
  wins_exclusively = False

  def __init__(self, name, *, must_lynch=1):
    super().__init__(name)
    self.must_lynch = must_lynch

  def fate(self, **kwargs):
    living  = len(self.members)
    lynched = len([p for p in self.all_members if self.game.log.has_been_lynched(p)])

    if lynched >= self.must_lynch:         return Fate.won
    if living + lynched < self.must_lynch: return Fate.lost
    return Fate.undecided

  @property
  def objective(self):
    if len(self.members) == 1:
      return "You win if you get lynched."
    else:
      return "You win if at least %d of you and your joker buddies get lynched." % self.must_lynch

class LyncherFaction(Faction):
  adjective        = "Third Party"
  alignment        = Alignment.evil
  is_town_enemy    = False
  is_town_friend   = False
  wins_exclusively = False

  def set_target(self, lynchee):
    self.lynchee = lynchee

  def fate(self, **kwargs):
    if self.lynchee.alive: return Fate.undecided
    return Fate.won if self.game.log.has_been_lynched(self.lynchee) else Fate.lost

  @property
  def objective(self):
    return "You win if %s gets lynched." % self.lynchee

class Mafia(Faction):
  adjective      = "Mafia"
  alignment      = Alignment.evil
  is_town_enemy  = True
  is_town_friend = False
  objective      = "You win if your mafia accounts for half or more of the surviving players."

  def fate(self, **kwargs):
    if len(self.members) == 0: return Fate.lost
    if 2 * len(self.members) >= len(self.game.players): return Fate.won
    return Fate.undecided

class Masonry(Faction):
  adjective      = "Mason"
  alignment      = Alignment.good
  is_town_enemy  = False
  is_town_friend = True
  objective      = Town.objective

  def __init__(self, name, town):
    super().__init__(name)
    self.town = town

  @property
  def alignment(self):
    return self.town.alignment

  def fate(self, **kwargs):
    return self.town.fate(**kwargs)
