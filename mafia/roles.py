from .actions import *
from .placeholders import *

class Role(object):
  def __init__(self, *, faction):
    self.faction = faction

  def __str__(self):
    return "%s %s" % (str(self.faction), self.__class__.__name__)

  @property
  def alignment(self):
    return self.faction.alignment

  @property
  def action(self):
    return None

class Villager(Role):
  pass

class Goon(Role):
  pass

class Godfather(Role):
  alignment = "good"

class Doctor(Role):
  action = Protect(Placeholder.Player())

class Cop(Role):
  action = Investigate(Placeholder.Player())

class Tracker(Role):
  action = Track(Placeholder.Player())

class Watcher(Role):
  action = Watch(Placeholder.Player())

class ForensicInvestigator(Role):
  action = Autopsy(Placeholder.Player())

class Roleblocker(Role):
  action = Roleblock(Placeholder.Player())

class Busdriver(Role):
  action = Busdrive(Placeholder.Player(), Placeholder.Player())
