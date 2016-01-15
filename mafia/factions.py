class Faction(object):
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return self.__class__.__name__

class Town(Faction):
  alignment = "good"

  def __init__(self):
    super().__init__("Town")

class Mafia(Faction):
  alignment = "evil"
