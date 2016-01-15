class Role(object):
  def __init__(self, *, faction):
    self.faction = faction

  def __str__(self):
    return "%s %s" % (str(self.faction), self.__class__.__name__)

class Villager(Role):
  pass

class Goon(Role):
  pass

class Cop(Role):
  pass

class Doctor(Role):
  pass
