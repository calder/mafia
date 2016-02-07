from .actions import *
from .factions import *
from . import placeholders
from .player import *
from .virtual_actions import *

import copy
import re

class RoleBase(object):
  adjectives  = []
  actions     = []
  action      = None
  protectable = True  # Whether the role respects doctors
  blockable   = True  # Whether the role respects roleblockers
  visible     = True  # Whether the role respects trackers, watchers, and forensic investigators
  votes       = 1     # The number of votes the player gets during the day

  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.faction       = faction
    self.fake_factions = []

  @property
  def apparent_factions(self):
    return [self.faction] + self.fake_factions

  @property
  def alignment(self):
    return self.faction.alignment

  @property
  def apparent_alignment(self):
    return self.alignment

  @property
  def wins_exclusively(self):
    return self.faction.wins_exclusively

  def fate(self, game):
    return self.faction.fate(game)

class Role(object):
  def __init__(self, faction_or_role):
    if isinstance(faction_or_role, Faction):
      faction_or_role = RoleBase(faction_or_role)
    assert isinstance(faction_or_role, Role) or isinstance(faction_or_role, RoleBase)
    self.base = faction_or_role

    # Prevent accidental modification of a class's prototypical action
    self.action = copy.deepcopy(self.action)

  def __getattr__(self, attr):
    return getattr(self.base, attr)

  def __str__(self):
    return "%s %s" % (self.faction.adjective, " ".join(self.adjectives))

  @property
  def adjectives(self):
    return [self.adjective] + self.base.adjectives

  @property
  def adjective(self):
    return " ".join(re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__))

  @property
  def actions(self):
    if self.action: return [self.action] + self.base.actions
    return self.base.actions

class ActionDoubler(Role):
  action = Double(placeholders.Self(), placeholders.Player())

class Busdriver(Role):
  action = Busdrive(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Cop(Role):
  action = Investigate(placeholders.Self(), placeholders.Player())

class Doctor(Role):
  action = Protect(placeholders.Self(), placeholders.Player())

class DoubleVoter(Role):
  votes = 2

class ForensicInvestigator(Role):
  action = Autopsy(placeholders.Self(), placeholders.Corpse())

class Godfather(Role):
  apparent_alignment = Alignment.good

class Goon(Role):
  pass

class Hitman(Role):
  protectable = False

class Joker(Role):
  def __init__(self, faction=None):
    faction = faction or JokerFaction("Solo Joker")
    super().__init__(faction)

class Lyncher(Role):
  def __init__(self, lynchee_or_lyncher_faction):
    if isinstance(lynchee_or_lyncher_faction, Player):
      faction_name = "%s Lyncher" % lynchee_or_lyncher_faction
      faction = LyncherFaction(faction_name, lynchee_or_lyncher_faction)
    else:
      faction = lynchee_or_lyncher_faction
    super().__init__(faction)

class Mason(Role):
  pass

class Miller(Role):
  apparent_alignment = Alignment.evil

class Ninja(Role):
  visible = False

class Politician(Role):
  action = StealVote(placeholders.Self(), placeholders.Player())

class Roleblocker(Role):
  action = Roleblock(placeholders.Self(), placeholders.Player())

class Tracker(Role):
  action = Track(placeholders.Self(), placeholders.Player())

class Usurper(Role):
  def __init__(self, faction, usurpee):
    super().__init__(faction)
    self.usurpee = usurpee

  def fate(self, game):
    faction_fate = self.faction.fate(game)
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  action = Watch(placeholders.Self(), placeholders.Player())

class Ventriloquist(Role):
  action = Possess(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Villager(Role):
  pass
