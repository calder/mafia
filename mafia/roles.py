from .actions import *
from .factions import *
from .virtual_actions import *
from .placeholders import *

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

  def fate(self, all_players):
    return self.faction.fate(all_players)

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
  action = Double(Placeholder.Self(), Placeholder.Player())

class Busdriver(Role):
  action = Busdrive(Placeholder.Self(), Placeholder.Player(), Placeholder.Player())

class Cop(Role):
  action = Investigate(Placeholder.Self(), Placeholder.Player())

class Doctor(Role):
  action = Protect(Placeholder.Self(), Placeholder.Player())

class DoubleVoter(Role):
  votes = 2

class ForensicInvestigator(Role):
  action = Autopsy(Placeholder.Self(), Placeholder.Corpse())

class Godfather(Role):
  alignment = Alignment.good

class Goon(Role):
  pass

class Hitman(Role):
  protectable = False

class Mason(Role):
  pass

class Ninja(Role):
  visible = False

class Politician(Role):
  action = StealVote(Placeholder.Self(), Placeholder.Player())

class Roleblocker(Role):
  action = Roleblock(Placeholder.Self(), Placeholder.Player())

class Tracker(Role):
  action = Track(Placeholder.Self(), Placeholder.Player())

class Usurper(Role):
  def __init__(self, faction, usurpee):
    super().__init__(faction)
    self.usurpee = usurpee

  def fate(self, all_players):
    faction_fate = self.faction.fate(all_players)
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  action = Watch(Placeholder.Self(), Placeholder.Player())

class Ventriloquist(Role):
  action = Possess(Placeholder.Self(), Placeholder.Player(), Placeholder.Player())

class Villager(Role):
  pass
