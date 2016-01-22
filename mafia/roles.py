from .actions import *
from .factions import *
from .virtual_actions import *
from .placeholders import *

import copy

class Role(object):
  action      = None
  protectable = True  # Whether the role respects doctors
  blockable   = True  # Whether the role respects roleblockers
  visible     = True  # Whether the role respects trackers, watchers, and forensic investigators
  votes       = 1     # The number of votes the player gets during the day

  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.faction = faction

    # Prevent accidental modification of a class's prototypical action
    self.action = copy.deepcopy(self.action)

  def __str__(self):
    return "%s %s" % (str(self.faction), self.__class__.__name__)

  @property
  def alignment(self):
    return self.faction.alignment

class Villager(Role):
  pass

class Goon(Role):
  rank = 100

class Godfather(Role):
  rank = 1
  alignment = Alignment.good

class Usurper(Role):
  rank = 2

class Doctor(Role):
  rank = 20
  action = Protect(Placeholder.Self(), Placeholder.Player())

class Cop(Role):
  rank = 30
  action = Investigate(Placeholder.Self(), Placeholder.Player())

class Tracker(Role):
  rank = 41
  action = Track(Placeholder.Self(), Placeholder.Player())

class Watcher(Role):
  rank = 42
  action = Watch(Placeholder.Self(), Placeholder.Player())

class ForensicInvestigator(Role):
  rank = 40
  action = Autopsy(Placeholder.Self(), Placeholder.Corpse())

class Roleblocker(Role):
  rank = 51
  action = Roleblock(Placeholder.Self(), Placeholder.Player())

class Busdriver(Role):
  rank = 50
  action = Busdrive(Placeholder.Self(), Placeholder.Player(), Placeholder.Player())

class Hitman(Role):
  rank = 3
  doctorable = False

class Ninja(Role):
  rank = 4
  visible = False
