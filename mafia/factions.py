from .actions import *
from .virtual_actions import *
from .placeholders import *

class Faction(object):
  action = NoAction()

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

  def __init__(self, name):
    super().__init__(name)
    self.action = Kill(Placeholder.FactionMember(self), Placeholder.Player())
