from .util import *

PUBLIC = SingletonValue()

class Event(object):
  def __init__(self):
    self.phase  = None  # Filled in by State.log
    self.to     = None  # None, a player, a faction, or PUBLIC

  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

  def __str__(self):
    if self.to is None:
      return "%s: [%s]" % (self.phase, self._str())
    elif self.to is PUBLIC:
      return "%s: %s" % (self.phase, self._str())
    else:
      return "%s: %s: %s" % (self.phase, self.to, self._str())

class Targetted(Event):
  def __init__(self, player, target):
    super().__init__()
    self.player = player
    self.target = target

  def _str(self):
    return "%s targetted %s." % (self.player, self.target)

class Blocked(Event):
  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was blocked." % self.player

class Saved(Event):
  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was saved." % self.player

class Died(Event):
  def __init__(self, player):
    super().__init__()
    self.player = player
    self.to     = PUBLIC

  def _str(self):
    return "%s, the %s, has died." % (self.player, self.player.role)

class TurntUp(Event):
  def __init__(self, player, alignment, *, to):
    super().__init__()
    self.player = player
    self.alignment = alignment
    self.to = to

  def _str(self):
    return "%s is %s." % (self.player, self.alignment)
