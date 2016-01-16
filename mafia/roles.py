class Role(object):
  def __init__(self, *, faction):
    self.faction = faction

  def __str__(self):
    return "%s %s" % (str(self.faction), self.__class__.__name__)

  @property
  def alignment(self):
    return self.faction.alignment

  @property
  def actions(self):
    return []

class Villager(Role):
  pass

class Goon(Role):
  pass

class Godfather(Role):
  alignment = "good"

class Doctor(Role):
  pass

class Cop(Role):
  pass

class Tracker(Role):
  pass

class Watcher(Role):
  pass

class ForensicInvestigator(Role):
  pass

class Roleblocker(Role):
  pass

class Busdriver(Role):
  pass
