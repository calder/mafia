from .actions import *
from .factions import *
from .virtual_actions import *
from .placeholders import *

import copy
import re

class Role(object):
  action      = None
  protectable = True  # Whether the role respects doctors
  blockable   = True  # Whether the role respects roleblockers
  visible     = True  # Whether the role respects trackers, watchers, and forensic investigators
  votes       = 1     # The number of votes the player gets during the day

  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.faction       = faction
    self.fake_factions = []

    # Prevent accidental modification of a class's prototypical action
    self.action = copy.deepcopy(self.action)

  def __str__(self):
    return "%s %s" % (str(self.faction.adjective), self.name)

  @property
  def name(self):
    return " ".join(re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__))

  @property
  def apparent_factions(self):
    return [self.faction]

  @property
  def alignment(self):
    return self.faction.alignment

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

class Watcher(Role):
  action = Watch(Placeholder.Self(), Placeholder.Player())

class Ventriloquist(Role):
  action = Possess(Placeholder.Self(), Placeholder.Player(), Placeholder.Player())

class Villager(Role):
  pass
